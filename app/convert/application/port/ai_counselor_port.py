from abc import ABC, abstractmethod

from app.convert.domain.analysis import Analysis
from app.shared.domain.user_profile import UserProfile


class AICounselorPort(ABC):
    """AI 상담사 포트 인터페이스

    상담 분석 생성을 담당하는 외부 AI 서비스와의 계약
    """

    @abstractmethod
    def generate_analysis(
        self, profile: UserProfile, conversation_history: list[dict]
    ) -> Analysis:
        """대화 내용을 기반으로 MBTI 관계 분석 결과를 생성한다

        Args:
            profile: 사용자의 프로필 (MBTI, Gender)
            conversation_history: 대화 내역 리스트
                [{"role": "user", "content": "..."}, {"role": "assistant", "content": "..."}]

        Returns:
            Analysis: 4개 섹션을 포함한 분석 결과
        """
        raise NotImplementedError
