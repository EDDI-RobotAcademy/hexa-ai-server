from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass
class OAuthUserInfo:
    """OAuth provider에서 받은 사용자 정보"""

    provider: str
    provider_user_id: str
    email: str


class OAuthProviderPort(ABC):
    """OAuth provider 포트 인터페이스"""

    @abstractmethod
    def get_user_info(self, code: str) -> OAuthUserInfo | None:
        """
        authorization code로 사용자 정보를 조회한다.

        Args:
            code: OAuth authorization code

        Returns:
            OAuthUserInfo: 성공시 사용자 정보, 실패시 None
        """
        pass

    @abstractmethod
    def get_authorization_url(self, redirect_uri: str, state: str) -> str:
        """
        OAuth 인증 URL을 생성한다.

        Args:
            redirect_uri: 콜백 URL
            state: CSRF 방지용 state

        Returns:
            str: OAuth 인증 URL
        """
        pass