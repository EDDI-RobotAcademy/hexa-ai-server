class Analysis:
    """상담 분석 결과 도메인 객체

    3턴 상담 완료 후 생성되는 MBTI 기반 관계 분석 결과
    """

    def __init__(self, situation: str, traits: str, solutions: str, cautions: str):
        """Analysis 객체 생성

        Args:
            situation: 상황 정리
            traits: MBTI 특성 분석
            solutions: 관계 개선 솔루션
            cautions: 주의사항

        Raises:
            ValueError: 필수 필드가 None이거나 빈 문자열일 경우
        """
        if situation is None or situation == "":
            raise ValueError("상황 정리는 필수입니다")
        if traits is None or traits == "":
            raise ValueError("MBTI 특성은 필수입니다")
        if solutions is None or solutions == "":
            raise ValueError("솔루션은 필수입니다")
        if cautions is None or cautions == "":
            raise ValueError("주의사항은 필수입니다")

        self._situation = situation
        self._traits = traits
        self._solutions = solutions
        self._cautions = cautions

    @property
    def situation(self) -> str:
        """상황 정리"""
        return self._situation

    @property
    def traits(self) -> str:
        """MBTI 특성 분석"""
        return self._traits

    @property
    def solutions(self) -> str:
        """관계 개선 솔루션"""
        return self._solutions

    @property
    def cautions(self) -> str:
        """주의사항"""
        return self._cautions
