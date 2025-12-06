import pytest
from app.shared.domain.gender import Gender


def test_gender_creates_from_valid_string():
    """유효한 Gender 문자열로 객체를 생성할 수 있다"""
    # Given: 유효한 Gender 문자열
    male = "MALE"
    female = "FEMALE"

    # When: Gender 객체를 생성하면
    gender_male = Gender(male)
    gender_female = Gender(female)

    # Then: 정상적으로 생성되고 값을 조회할 수 있다
    assert gender_male.value == "MALE"
    assert gender_female.value == "FEMALE"


def test_gender_accepts_case_insensitive_input():
    """대소문자 구분 없이 Gender를 생성할 수 있다"""
    # Given: 다양한 대소문자 조합의 Gender 문자열
    inputs = ["male", "Male", "MALE", "female", "Female", "FEMALE"]

    # When & Then: 모두 정상적으로 생성되고 대문자로 저장된다
    assert Gender(inputs[0]).value == "MALE"
    assert Gender(inputs[1]).value == "MALE"
    assert Gender(inputs[2]).value == "MALE"
    assert Gender(inputs[3]).value == "FEMALE"
    assert Gender(inputs[4]).value == "FEMALE"
    assert Gender(inputs[5]).value == "FEMALE"


def test_gender_rejects_invalid_values():
    """유효하지 않은 Gender 값을 거부한다"""
    # Given: 유효하지 않은 Gender 문자열들
    invalid_genders = ["MAN", "WOMAN", "M", "F", "OTHER", "", "UNKNOWN"]

    # When & Then: Gender 객체 생성 시 ValueError가 발생한다
    for invalid_gender in invalid_genders:
        with pytest.raises(ValueError):
            Gender(invalid_gender)
