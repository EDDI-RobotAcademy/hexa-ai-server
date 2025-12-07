from urllib.parse import urlencode

from app.auth.application.port.oauth_provider_port import OAuthProviderPort, OAuthUserInfo


class InMemoryOAuthProvider(OAuthProviderPort):
    """테스트용 In-Memory OAuth provider"""

    def __init__(
        self,
        provider_name: str,
        users: dict[str, OAuthUserInfo] | None = None,
        auth_url: str = "https://oauth.example.com/auth",
    ):
        self._provider_name = provider_name
        self._users = users or {}
        self._auth_url = auth_url

    def get_user_info(self, code: str) -> OAuthUserInfo | None:
        """code로 사용자 정보 조회"""
        return self._users.get(code)

    def get_authorization_url(self, redirect_uri: str, state: str) -> str:
        """OAuth 인증 URL 생성"""
        params = {
            "redirect_uri": redirect_uri,
            "state": state,
        }
        return f"{self._auth_url}?{urlencode(params)}"