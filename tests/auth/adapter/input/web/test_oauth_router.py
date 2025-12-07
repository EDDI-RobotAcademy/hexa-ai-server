import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from app.auth.adapter.input.web import oauth_router as oauth_router_module
from app.auth.adapter.input.web.oauth_router import (
    oauth_router,
    register_oauth_provider,
    set_oauth_callback_use_case,
    _state_storage,
)
from app.auth.application.port.oauth_provider_port import OAuthUserInfo
from app.auth.application.use_case.oauth_callback_use_case import (
    OAuthCallbackResult,
    OAuthCallbackUseCase,
)
from app.auth.infrastructure.oauth.in_memory_oauth_provider import InMemoryOAuthProvider
from unittest.mock import Mock


@pytest.fixture
def app():
    """테스트용 FastAPI 앱"""
    test_app = FastAPI()
    test_app.include_router(oauth_router, prefix="/auth")
    return test_app


@pytest.fixture
def client(app):
    """테스트 클라이언트"""
    return TestClient(app)


@pytest.fixture(autouse=True)
def setup_providers():
    """각 테스트 전에 provider 설정"""
    # Clear state storage
    _state_storage.clear()

    # Register test provider
    test_provider = InMemoryOAuthProvider(
        provider_name="google",
        users={
            "valid_code": OAuthUserInfo(
                provider="google",
                provider_user_id="google_123",
                email="test@example.com",
            )
        },
        auth_url="https://accounts.google.com/o/oauth2/auth",
    )
    register_oauth_provider("google", test_provider)

    # Register mock use case
    mock_use_case = Mock(spec=OAuthCallbackUseCase)
    mock_use_case.execute.return_value = OAuthCallbackResult(session_id="test-session-123")
    set_oauth_callback_use_case(mock_use_case)

    yield

    # Cleanup
    oauth_router_module._oauth_providers.clear()
    oauth_router_module._oauth_callback_use_case = None
    _state_storage.clear()


class TestOAuthLoginUrl:
    """OAuth 로그인 URL 테스트"""

    def test_로그인_url_반환(self, client):
        """OAuth 로그인 URL을 반환한다"""
        response = client.get(
            "/auth/google/login",
            params={"redirect_uri": "http://localhost:3000/callback"},
        )

        assert response.status_code == 200
        data = response.json()
        assert "url" in data
        assert "accounts.google.com" in data["url"]

    def test_지원하지_않는_provider_에러(self, client):
        """지원하지 않는 provider면 400 에러"""
        response = client.get(
            "/auth/unknown/login",
            params={"redirect_uri": "http://localhost:3000/callback"},
        )

        assert response.status_code == 400
        assert "지원하지 않는" in response.json()["detail"]


class TestOAuthCallback:
    """OAuth 콜백 테스트"""

    def test_유효한_콜백_세션_반환(self, client):
        """유효한 OAuth 콜백이면 세션 ID 반환"""
        # First, get a valid state
        login_response = client.get(
            "/auth/google/login",
            params={"redirect_uri": "http://localhost:3000/callback"},
        )
        url = login_response.json()["url"]
        # Extract state from URL
        state = url.split("state=")[1].split("&")[0] if "state=" in url else None
        assert state is not None

        # Then, use the state in callback
        response = client.get(
            "/auth/google/callback",
            params={"code": "valid_code", "state": state},
        )

        assert response.status_code == 200
        data = response.json()
        assert data["session_id"] == "test-session-123"

    def test_유효하지_않은_state_에러(self, client):
        """유효하지 않은 state면 400 에러"""
        response = client.get(
            "/auth/google/callback",
            params={"code": "valid_code", "state": "invalid_state"},
        )

        assert response.status_code == 400
        assert "state" in response.json()["detail"]

    def test_유효하지_않은_code_에러(self, client):
        """유효하지 않은 code면 400 에러"""
        # First, get a valid state
        login_response = client.get(
            "/auth/google/login",
            params={"redirect_uri": "http://localhost:3000/callback"},
        )
        url = login_response.json()["url"]
        state = url.split("state=")[1].split("&")[0] if "state=" in url else None

        # Then, use invalid code
        response = client.get(
            "/auth/google/callback",
            params={"code": "invalid_code", "state": state},
        )

        assert response.status_code == 400
        assert "인증에 실패" in response.json()["detail"]
