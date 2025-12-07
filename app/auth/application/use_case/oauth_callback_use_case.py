import uuid
from dataclasses import dataclass

from app.auth.application.port.oauth_identity_repository_port import (
    OAuthIdentityRepositoryPort,
)
from app.auth.application.port.session_repository_port import SessionRepositoryPort
from app.auth.domain.oauth_identity import OAuthIdentity
from app.auth.domain.session import Session
from app.user.application.port.user_repository_port import UserRepositoryPort
from app.user.domain.user import User


@dataclass
class OAuthCallbackResult:
    """OAuth 콜백 처리 결과"""

    session_id: str


class OAuthCallbackUseCase:
    """OAuth 콜백 처리 유스케이스"""

    def __init__(
        self,
        oauth_identity_repo: OAuthIdentityRepositoryPort,
        user_repo: UserRepositoryPort,
        session_repo: SessionRepositoryPort,
    ):
        self._oauth_identity_repo = oauth_identity_repo
        self._user_repo = user_repo
        self._session_repo = session_repo

    def execute(
        self, provider: str, provider_user_id: str, email: str
    ) -> OAuthCallbackResult:
        """
        OAuth 콜백을 처리한다.

        1. OAuthIdentity 존재 여부 확인
        2. 없으면 User 조회/생성 후 OAuthIdentity 생성
        3. Session 생성 및 반환
        """
        # 유효성 검증 (OAuthIdentity 도메인 생성으로 검증)
        OAuthIdentity(
            provider=provider, provider_user_id=provider_user_id, email=email
        )

        # 기존 OAuthIdentity 조회
        existing_identity = (
            self._oauth_identity_repo.find_by_provider_and_provider_user_id(
                provider=provider, provider_user_id=provider_user_id
            )
        )

        if existing_identity:
            # 기존 OAuth 사용자 → User 조회
            user = self._user_repo.find_by_email(existing_identity.email)
        else:
            # 신규 OAuth → User 조회 또는 생성
            user = self._user_repo.find_by_email(email)
            if not user:
                user = User(id=str(uuid.uuid4()), email=email)
                self._user_repo.save(user)

            # 새 OAuthIdentity 생성
            new_identity = OAuthIdentity(
                provider=provider, provider_user_id=provider_user_id, email=email
            )
            self._oauth_identity_repo.save(new_identity)

        # Session 생성
        session = Session(session_id=str(uuid.uuid4()), user_id=user.id)
        self._session_repo.save(session)

        return OAuthCallbackResult(session_id=session.session_id)