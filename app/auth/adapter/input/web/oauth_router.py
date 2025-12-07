import secrets

from fastapi import APIRouter, HTTPException, Query, status
from fastapi.responses import RedirectResponse

from app.auth.adapter.input.web.response.oauth_response import (
    OAuthCallbackResponse,
    OAuthLoginUrlResponse,
)
from app.auth.application.port.oauth_provider_port import OAuthProviderPort
from app.auth.application.use_case.oauth_callback_use_case import OAuthCallbackUseCase

oauth_router = APIRouter()

# Provider registry - will be populated by dependency injection
_oauth_providers: dict[str, OAuthProviderPort] = {}
_oauth_callback_use_case: OAuthCallbackUseCase | None = None

# State storage for CSRF protection (in-memory for now, should use Redis in production)
_state_storage: dict[str, bool] = {}


def register_oauth_provider(provider_name: str, provider: OAuthProviderPort) -> None:
    """OAuth provider 등록"""
    _oauth_providers[provider_name] = provider


def set_oauth_callback_use_case(use_case: OAuthCallbackUseCase) -> None:
    """OAuth 콜백 유스케이스 설정"""
    global _oauth_callback_use_case
    _oauth_callback_use_case = use_case


def _get_provider(provider: str) -> OAuthProviderPort:
    """provider 이름으로 OAuth provider 조회"""
    if provider not in _oauth_providers:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"지원하지 않는 OAuth provider입니다: {provider}",
        )
    return _oauth_providers[provider]


@oauth_router.get(
    "/{provider}/login",
    response_model=OAuthLoginUrlResponse,
)
def get_oauth_login_url(
    provider: str,
    redirect_uri: str = Query(..., description="OAuth 콜백 후 리다이렉트할 URL"),
) -> OAuthLoginUrlResponse:
    """
    OAuth 로그인 URL을 반환합니다.
    """
    oauth_provider = _get_provider(provider)

    # CSRF 방지용 state 생성
    state = secrets.token_urlsafe(32)
    _state_storage[state] = True

    url = oauth_provider.get_authorization_url(
        redirect_uri=redirect_uri,
        state=state,
    )

    return OAuthLoginUrlResponse(url=url)


@oauth_router.get(
    "/{provider}/callback",
    response_model=OAuthCallbackResponse,
)
def oauth_callback(
    provider: str,
    code: str = Query(..., description="OAuth authorization code"),
    state: str = Query(..., description="CSRF 방지용 state"),
) -> OAuthCallbackResponse:
    """
    OAuth 콜백을 처리하고 세션을 생성합니다.
    """
    # CSRF 검증
    if state not in _state_storage:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="유효하지 않은 state입니다",
        )
    del _state_storage[state]

    # OAuth provider에서 사용자 정보 조회
    oauth_provider = _get_provider(provider)
    user_info = oauth_provider.get_user_info(code)

    if not user_info:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="OAuth 인증에 실패했습니다",
        )

    # 유스케이스 실행
    if not _oauth_callback_use_case:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="OAuth 콜백 유스케이스가 설정되지 않았습니다",
        )

    result = _oauth_callback_use_case.execute(
        provider=user_info.provider,
        provider_user_id=user_info.provider_user_id,
        email=user_info.email,
    )

    return OAuthCallbackResponse(session_id=result.session_id)
