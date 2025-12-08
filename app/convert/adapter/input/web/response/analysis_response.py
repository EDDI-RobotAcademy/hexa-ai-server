from pydantic import BaseModel

from app.convert.domain.analysis import Analysis


class AnalysisResponse(BaseModel):
    """분석 결과 응답 DTO"""

    situation: str
    traits: str
    solutions: str
    cautions: str

    @staticmethod
    def from_domain(analysis: Analysis) -> "AnalysisResponse":
        """도메인 객체를 DTO로 변환

        Args:
            analysis: Analysis 도메인 객체

        Returns:
            AnalysisResponse DTO
        """
        return AnalysisResponse(
            situation=analysis.situation,
            traits=analysis.traits,
            solutions=analysis.solutions,
            cautions=analysis.cautions,
        )

    class Config:
        json_schema_extra = {
            "example": {
                "situation": "직장 상사와의 소통에 어려움을 겪고 있습니다.",
                "traits": "INTJ는 논리적이고 독립적인 성향입니다.",
                "solutions": "감정을 먼저 공감하는 연습을 해보세요.",
                "cautions": "논리적인 태도가 냉정하게 느껴질 수 있습니다.",
            }
        }
