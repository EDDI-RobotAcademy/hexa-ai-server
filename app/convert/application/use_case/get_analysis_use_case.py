from app.convert.application.port.consult_repository_port import ConsultRepositoryPort
from app.convert.application.port.ai_counselor_port import AICounselorPort
from app.convert.domain.analysis import Analysis


class GetAnalysisUseCase:
    """상담 분석 결과 조회 유스케이스"""

    def __init__(self, repository: ConsultRepositoryPort, counselor: AICounselorPort):
        """GetAnalysisUseCase 생성

        Args:
            repository: 세션 저장소
            counselor: AI 상담사
        """
        self._repository = repository
        self._counselor = counselor

    def execute(self, session_id: str) -> Analysis:
        """세션 ID로 분석 결과를 조회

        Args:
            session_id: 조회할 세션 ID

        Returns:
            Analysis: 분석 결과

        Raises:
            ValueError: 세션을 찾을 수 없거나 상담이 완료되지 않은 경우
        """
        # 세션 조회
        session = self._repository.find_by_id(session_id)
        if session is None:
            raise ValueError("세션을 찾을 수 없습니다")

        # 3턴 완료 검증
        if not session.is_completed():
            raise ValueError("상담이 아직 완료되지 않았습니다")

        # AI 분석 생성
        conversation_history = session.get_conversation_history()
        analysis = self._counselor.generate_analysis(
            profile=session.profile, conversation_history=conversation_history
        )

        return analysis
