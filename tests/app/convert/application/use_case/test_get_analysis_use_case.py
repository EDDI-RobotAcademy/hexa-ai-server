import pytest
from typing import Optional
from app.convert.application.use_case.get_analysis_use_case import GetAnalysisUseCase
from app.convert.application.port.ai_counselor_port import AICounselorPort
from app.convert.application.port.consult_repository_port import ConsultRepositoryPort
from app.convert.domain.consult_session import ConsultSession
from app.convert.domain.message import Message
from app.convert.domain.analysis import Analysis
from app.shared.domain.user_profile import UserProfile
from app.shared.domain.gender import Gender
from app.shared.domain.mbti import MBTI


class FakeConsultRepository(ConsultRepositoryPort):
    """테스트용 Fake Repository"""

    def __init__(self):
        self.sessions = {}

    def save(self, session: ConsultSession) -> ConsultSession:
        self.sessions[session.session_id] = session
        return session

    def find_by_id(self, session_id: str) -> Optional[ConsultSession]:
        return self.sessions.get(session_id)


class FakeAICounselor(AICounselorPort):
    """테스트용 Fake AI Counselor"""

    def generate_analysis(
        self, profile: UserProfile, conversation_history: list[dict]
    ) -> Analysis:
        return Analysis(
            situation="테스트 상황 정리",
            traits="테스트 MBTI 특성",
            solutions="테스트 솔루션",
            cautions="테스트 주의사항",
        )


def test_get_analysis_returns_analysis_for_completed_session():
    """3턴 완료된 세션은 분석 결과를 반환한다"""
    # Given: 3턴 완료된 세션
    repository = FakeConsultRepository()
    counselor = FakeAICounselor()
    use_case = GetAnalysisUseCase(repository=repository, counselor=counselor)

    profile = UserProfile(gender=Gender("FEMALE"), mbti=MBTI("INTJ"))
    session = ConsultSession(user_id="user-123", profile=profile)
    session.add_message(Message(role="user", content="질문1"))
    session.add_message(Message(role="assistant", content="답변1"))
    session.add_message(Message(role="user", content="질문2"))
    session.add_message(Message(role="assistant", content="답변2"))
    session.add_message(Message(role="user", content="질문3"))
    session.add_message(Message(role="assistant", content="답변3"))
    repository.save(session)

    # When: GetAnalysisUseCase를 실행하면
    analysis = use_case.execute(session_id=session.session_id)

    # Then: Analysis 객체가 반환된다
    assert isinstance(analysis, Analysis)
    assert analysis.situation == "테스트 상황 정리"
    assert analysis.traits == "테스트 MBTI 특성"
    assert analysis.solutions == "테스트 솔루션"
    assert analysis.cautions == "테스트 주의사항"


def test_get_analysis_raises_error_for_non_existent_session():
    """존재하지 않는 세션은 에러를 발생시킨다"""
    # Given: 빈 repository
    repository = FakeConsultRepository()
    counselor = FakeAICounselor()
    use_case = GetAnalysisUseCase(repository=repository, counselor=counselor)

    # When & Then: 존재하지 않는 session_id로 실행하면 ValueError 발생
    with pytest.raises(ValueError, match="세션을 찾을 수 없습니다"):
        use_case.execute(session_id="non-existent-id")


def test_get_analysis_raises_error_for_incomplete_session():
    """3턴 미완료 세션은 에러를 발생시킨다"""
    # Given: 2턴만 완료된 세션
    repository = FakeConsultRepository()
    counselor = FakeAICounselor()
    use_case = GetAnalysisUseCase(repository=repository, counselor=counselor)

    profile = UserProfile(gender=Gender("MALE"), mbti=MBTI("ENFP"))
    session = ConsultSession(user_id="user-123", profile=profile)
    session.add_message(Message(role="user", content="질문1"))
    session.add_message(Message(role="assistant", content="답변1"))
    session.add_message(Message(role="user", content="질문2"))
    repository.save(session)

    # When & Then: 미완료 세션으로 실행하면 ValueError 발생
    with pytest.raises(ValueError, match="상담이 아직 완료되지 않았습니다"):
        use_case.execute(session_id=session.session_id)
