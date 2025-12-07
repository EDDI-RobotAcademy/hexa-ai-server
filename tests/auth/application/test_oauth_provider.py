import pytest

from app.auth.application.port.oauth_provider_port import OAuthProviderPort, OAuthUserInfo
from app.auth.infrastructure.oauth.in_memory_oauth_provider import InMemoryOAuthProvider


class TestOAuthProviderPort:
    """OAuth Provider Port 테스트"""

    def test_get_user_info_returns_oauth_user_info(self):
        """authorization code로 사용자 정보를 조회한다"""
        # Given: OAuth provider와 유효한 code
        provider = InMemoryOAuthProvider(
            provider_name="google",
            users={
                "valid_code": OAuthUserInfo(
                    provider="google",
                    provider_user_id="google_123",
                    email="user@example.com",
                )
            },
        )

        # When: code로 사용자 정보 조회
        user_info = provider.get_user_info("valid_code")

        # Then: 사용자 정보 반환
        assert user_info is not None
        assert user_info.provider == "google"
        assert user_info.provider_user_id == "google_123"
        assert user_info.email == "user@example.com"

    def test_get_user_info_returns_none_for_invalid_code(self):
        """유효하지 않은 code면 None 반환"""
        # Given: OAuth provider
        provider = InMemoryOAuthProvider(provider_name="google", users={})

        # When: 유효하지 않은 code로 조회
        user_info = provider.get_user_info("invalid_code")

        # Then: None 반환
        assert user_info is None

    def test_get_authorization_url_returns_valid_url(self):
        """OAuth 인증 URL을 반환한다"""
        # Given: OAuth provider
        provider = InMemoryOAuthProvider(
            provider_name="google",
            users={},
            auth_url="https://accounts.google.com/o/oauth2/auth",
        )

        # When: 인증 URL 조회
        url = provider.get_authorization_url(
            redirect_uri="http://localhost:3000/callback",
            state="random_state",
        )

        # Then: 올바른 URL 형식 반환
        assert "https://accounts.google.com/o/oauth2/auth" in url
        assert "redirect_uri=" in url
        assert "localhost" in url
        assert "callback" in url
        assert "state=random_state" in url