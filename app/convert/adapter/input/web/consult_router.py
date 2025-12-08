from fastapi import APIRouter, HTTPException, status, Depends

from app.convert.adapter.input.web.response.analysis_response import AnalysisResponse
from app.convert.application.use_case.get_analysis_use_case import GetAnalysisUseCase

consult_router = APIRouter()


def get_analysis_use_case() -> GetAnalysisUseCase:
    """GetAnalysisUseCase 의존성 주입

    TODO: 실제 구현에서는 Repository와 AICounselor를 주입해야 함
    """
    # 이 부분은 나중에 실제 의존성으로 교체 필요
    raise NotImplementedError("의존성 주입이 필요합니다")


@consult_router.get(
    "/{session_id}/analysis",
    response_model=AnalysisResponse,
    status_code=status.HTTP_200_OK,
    summary="상담 분석 결과 조회",
    description="3턴 완료된 상담 세션의 MBTI 기반 분석 결과를 조회합니다",
)
def get_analysis(
    session_id: str,
    use_case: GetAnalysisUseCase = Depends(get_analysis_use_case),
):
    """상담 분석 결과 조회

    Args:
        session_id: 세션 ID
        use_case: GetAnalysisUseCase (의존성 주입)

    Returns:
        AnalysisResponse: 분석 결과

    Raises:
        HTTPException: 세션을 찾을 수 없거나(404) 상담이 완료되지 않은 경우(400)
    """
    try:
        analysis = use_case.execute(session_id=session_id)
        return AnalysisResponse.from_domain(analysis)
    except ValueError as e:
        error_message = str(e)
        if "찾을 수 없습니다" in error_message:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail=error_message
            )
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail=error_message
            )
