import pytest
from app.shared.domain.mbti import MBTI


def test_mbti_creates_from_valid_string():
    """유효한 MBTI 문자열로 객체를 생성할 수 있다"""
    # Given: 유효한 MBTI 문자열
    mbti_string = "INTJ"

    # When: MBTI 객체를 생성하면
    mbti = MBTI(mbti_string)

    # Then: 정상적으로 생성되고 값을 조회할 수 있다
    assert mbti.value == "INTJ"
