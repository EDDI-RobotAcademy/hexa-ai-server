import pytest
from app.convert.application.port.ai_counselor_port import AICounselorPort
from app.convert.domain.analysis import Analysis
from app.shared.domain.user_profile import UserProfile
from app.shared.domain.gender import Gender
from app.shared.domain.mbti import MBTI


class FakeAICounselor(AICounselorPort):
    """테스트용 Fake AI Counselor"""

    def generate_analysis(
        self, profile: UserProfile, conversation_history: list[dict]
    ) -> Analysis:
        """대화 내용을 기반으로 분석 결과 생성"""
        return Analysis(
            situation="테스트 상황 정리",
            traits="테스트 MBTI 특성",
            solutions="테스트 솔루션",
            cautions="테스트 주의사항",
        )


def test_ai_counselor_port_generates_analysis_with_profile_and_history():
    """AICounselorPort는 프로필과 대화 내역을 받아 Analysis를 생성한다"""
    # Given: UserProfile과 대화 내역
    profile = UserProfile(gender=Gender("FEMALE"), mbti=MBTI("INTJ"))
    conversation_history = [
        {"role": "user", "content": "직장 상사와 갈등이 있어요"},
        {"role": "assistant", "content": "어떤 갈등인지 좀 더 말씀해주시겠어요?"},
        {"role": "user", "content": "제 의견을 무시하는 것 같아요"},
    ]

    # When: Fake AI Counselor로 분석 생성
    counselor = FakeAICounselor()
    analysis = counselor.generate_analysis(profile, conversation_history)

    # Then: Analysis 객체가 반환된다
    assert isinstance(analysis, Analysis)
    assert analysis.situation == "테스트 상황 정리"
    assert analysis.traits == "테스트 MBTI 특성"
    assert analysis.solutions == "테스트 솔루션"
    assert analysis.cautions == "테스트 주의사항"


def test_ai_counselor_port_is_abstract():
    """AICounselorPort는 추상 클래스로 직접 인스턴스화할 수 없다"""
    # When & Then: 직접 인스턴스화 시도하면 TypeError 발생
    with pytest.raises(TypeError):
        AICounselorPort()
