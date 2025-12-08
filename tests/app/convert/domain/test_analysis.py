import pytest
from app.convert.domain.analysis import Analysis


def test_analysis_creates_with_all_four_sections():
    """Analysis는 4개 섹션(상황, 특성, 솔루션, 주의사항)을 모두 가지고 생성된다"""
    # Given: 4개 섹션의 분석 내용
    situation = "사용자는 INTJ 성향으로 직장 상사와의 소통에 어려움을 겪고 있습니다."
    traits = "INTJ는 논리적이고 독립적인 성향으로 감정 표현에 서툴 수 있습니다."
    solutions = "상사와의 대화 시 논리보다는 감정을 먼저 공감하는 연습을 해보세요."
    cautions = "지나치게 논리적인 태도는 상대방에게 냉정하게 느껴질 수 있습니다."

    # When: Analysis 객체를 생성하면
    analysis = Analysis(
        situation=situation,
        traits=traits,
        solutions=solutions,
        cautions=cautions
    )

    # Then: 4개 섹션을 모두 조회할 수 있다
    assert analysis.situation == situation
    assert analysis.traits == traits
    assert analysis.solutions == solutions
    assert analysis.cautions == cautions


def test_analysis_rejects_none_situation():
    """situation이 None이면 생성을 거부한다"""
    # When & Then: situation이 None이면 ValueError가 발생한다
    with pytest.raises(ValueError, match="상황 정리는 필수입니다"):
        Analysis(
            situation=None,
            traits="INTJ 특성",
            solutions="해결책",
            cautions="주의사항"
        )


def test_analysis_rejects_empty_situation():
    """situation이 빈 문자열이면 생성을 거부한다"""
    # When & Then: situation이 빈 문자열이면 ValueError가 발생한다
    with pytest.raises(ValueError, match="상황 정리는 필수입니다"):
        Analysis(
            situation="",
            traits="INTJ 특성",
            solutions="해결책",
            cautions="주의사항"
        )


def test_analysis_rejects_none_traits():
    """traits가 None이면 생성을 거부한다"""
    # When & Then: traits가 None이면 ValueError가 발생한다
    with pytest.raises(ValueError, match="MBTI 특성은 필수입니다"):
        Analysis(
            situation="상황 정리",
            traits=None,
            solutions="해결책",
            cautions="주의사항"
        )


def test_analysis_rejects_empty_traits():
    """traits가 빈 문자열이면 생성을 거부한다"""
    # When & Then: traits가 빈 문자열이면 ValueError가 발생한다
    with pytest.raises(ValueError, match="MBTI 특성은 필수입니다"):
        Analysis(
            situation="상황 정리",
            traits="",
            solutions="해결책",
            cautions="주의사항"
        )


def test_analysis_rejects_none_solutions():
    """solutions가 None이면 생성을 거부한다"""
    # When & Then: solutions가 None이면 ValueError가 발생한다
    with pytest.raises(ValueError, match="솔루션은 필수입니다"):
        Analysis(
            situation="상황 정리",
            traits="INTJ 특성",
            solutions=None,
            cautions="주의사항"
        )


def test_analysis_rejects_empty_solutions():
    """solutions가 빈 문자열이면 생성을 거부한다"""
    # When & Then: solutions가 빈 문자열이면 ValueError가 발생한다
    with pytest.raises(ValueError, match="솔루션은 필수입니다"):
        Analysis(
            situation="상황 정리",
            traits="INTJ 특성",
            solutions="",
            cautions="주의사항"
        )


def test_analysis_rejects_none_cautions():
    """cautions가 None이면 생성을 거부한다"""
    # When & Then: cautions가 None이면 ValueError가 발생한다
    with pytest.raises(ValueError, match="주의사항은 필수입니다"):
        Analysis(
            situation="상황 정리",
            traits="INTJ 특성",
            solutions="해결책",
            cautions=None
        )


def test_analysis_rejects_empty_cautions():
    """cautions가 빈 문자열이면 생성을 거부한다"""
    # When & Then: cautions가 빈 문자열이면 ValueError가 발생한다
    with pytest.raises(ValueError, match="주의사항은 필수입니다"):
        Analysis(
            situation="상황 정리",
            traits="INTJ 특성",
            solutions="해결책",
            cautions=""
        )
