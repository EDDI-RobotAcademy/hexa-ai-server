import uuid
from unittest.mock import Mock

import pytest

from app.auth.application.port.oauth_identity_repository_port import (
    OAuthIdentityRepositoryPort,
)
from app.auth.application.port.session_repository_port import SessionRepositoryPort
from app.auth.application.use_case.oauth_callback_use_case import OAuthCallbackUseCase
from app.auth.domain.oauth_identity import OAuthIdentity
from app.auth.domain.session import Session
from app.user.application.port.user_repository_port import UserRepositoryPort
from app.user.domain.user import User


class TestOAuthCallbackUseCase:
    """OAuth 콜백 유스케이스 테스트"""

    def setup_method(self):
        """테스트 픽스처 설정"""
        self.oauth_identity_repo = Mock(spec=OAuthIdentityRepositoryPort)
        self.user_repo = Mock(spec=UserRepositoryPort)
        self.session_repo = Mock(spec=SessionRepositoryPort)
        self.use_case = OAuthCallbackUseCase(
            oauth_identity_repo=self.oauth_identity_repo,
            user_repo=self.user_repo,
            session_repo=self.session_repo,
        )

    def test_신규_사용자_oauth_콜백_처리시_유저와_세션_생성(self):
        """신규 사용자가 OAuth 로그인하면 User, OAuthIdentity, Session이 생성된다"""
        # Given: 존재하지 않는 OAuth 사용자
        self.oauth_identity_repo.find_by_provider_and_provider_user_id.return_value = (
            None
        )
        self.user_repo.find_by_email.return_value = None

        # When: OAuth 콜백 처리
        result = self.use_case.execute(
            provider="google",
            provider_user_id="google_123",
            email="new@example.com",
        )

        # Then: 새 User 저장됨
        self.user_repo.save.assert_called_once()
        saved_user = self.user_repo.save.call_args[0][0]
        assert isinstance(saved_user, User)
        assert saved_user.email == "new@example.com"

        # Then: 새 OAuthIdentity 저장됨
        self.oauth_identity_repo.save.assert_called_once()
        saved_identity = self.oauth_identity_repo.save.call_args[0][0]
        assert isinstance(saved_identity, OAuthIdentity)
        assert saved_identity.provider == "google"
        assert saved_identity.provider_user_id == "google_123"
        assert saved_identity.email == "new@example.com"

        # Then: 세션 생성됨
        self.session_repo.save.assert_called_once()
        saved_session = self.session_repo.save.call_args[0][0]
        assert isinstance(saved_session, Session)
        assert saved_session.user_id == saved_user.id

        # Then: 세션 ID 반환
        assert result.session_id == saved_session.session_id

    def test_기존_oauth_사용자_로그인시_새_세션만_생성(self):
        """기존 OAuth 사용자가 로그인하면 새 Session만 생성된다"""
        # Given: 이미 존재하는 OAuth 사용자
        existing_identity = OAuthIdentity(
            provider="google",
            provider_user_id="google_123",
            email="existing@example.com",
        )
        existing_user = User(id="user-123", email="existing@example.com")

        self.oauth_identity_repo.find_by_provider_and_provider_user_id.return_value = (
            existing_identity
        )
        self.user_repo.find_by_email.return_value = existing_user

        # When: OAuth 콜백 처리
        result = self.use_case.execute(
            provider="google",
            provider_user_id="google_123",
            email="existing@example.com",
        )

        # Then: User와 OAuthIdentity는 저장되지 않음
        self.user_repo.save.assert_not_called()
        self.oauth_identity_repo.save.assert_not_called()

        # Then: 세션만 생성됨
        self.session_repo.save.assert_called_once()
        saved_session = self.session_repo.save.call_args[0][0]
        assert saved_session.user_id == "user-123"

        # Then: 세션 ID 반환
        assert result.session_id is not None

    def test_기존_유저가_다른_oauth_provider로_로그인시_새_oauth_identity_생성(self):
        """이미 가입한 유저가 다른 OAuth provider로 로그인하면 새 OAuthIdentity만 추가"""
        # Given: 해당 OAuth는 없지만 이메일로 유저는 존재
        existing_user = User(id="user-123", email="user@example.com")

        self.oauth_identity_repo.find_by_provider_and_provider_user_id.return_value = (
            None
        )
        self.user_repo.find_by_email.return_value = existing_user

        # When: 새로운 OAuth provider로 콜백 처리
        result = self.use_case.execute(
            provider="kakao",
            provider_user_id="kakao_456",
            email="user@example.com",
        )

        # Then: User는 저장되지 않음 (이미 존재)
        self.user_repo.save.assert_not_called()

        # Then: 새 OAuthIdentity 저장됨
        self.oauth_identity_repo.save.assert_called_once()
        saved_identity = self.oauth_identity_repo.save.call_args[0][0]
        assert saved_identity.provider == "kakao"
        assert saved_identity.provider_user_id == "kakao_456"

        # Then: 기존 유저로 세션 생성
        self.session_repo.save.assert_called_once()
        saved_session = self.session_repo.save.call_args[0][0]
        assert saved_session.user_id == "user-123"

    def test_유효하지_않은_provider_에러(self):
        """유효하지 않은 provider면 ValueError 발생"""
        with pytest.raises(ValueError, match="provider"):
            self.use_case.execute(
                provider="invalid_provider",
                provider_user_id="123",
                email="test@example.com",
            )