class Analysis:
    """상담 분석 결과 도메인"""

    def __init__(
        self,
        situation: str,
        traits: str,
        solutions: str,
        cautions: str,
    ):
        self._validate(situation, traits, solutions, cautions)
        self.situation = situation
        self.traits = traits
        self.solutions = solutions
        self.cautions = cautions

    def _validate(self, situation: str, traits: str, solutions: str, cautions: str) -> None:
        if not situation or not situation.strip():
            raise ValueError("situation은 비어있을 수 없습니다")
        if not traits or not traits.strip():
            raise ValueError("traits는 비어있을 수 없습니다")
        if not solutions or not solutions.strip():
            raise ValueError("solutions는 비어있을 수 없습니다")
        if not cautions or not cautions.strip():
            raise ValueError("cautions는 비어있을 수 없습니다")

    def to_dict(self) -> dict:
        """Analysis를 dict로 변환한다"""
        return {
            "situation": self.situation,
            "traits": self.traits,
            "solutions": self.solutions,
            "cautions": self.cautions,
        }
