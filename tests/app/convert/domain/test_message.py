import pytest
from app.convert.domain.message import Message


def test_message_creates_with_role_and_content():
    """Message는 role과 content로 생성된다"""
    # Given: role과 content
    role = "user"
    content = "직장 상사와 갈등이 있어요"

    # When: Message 객체를 생성하면
    message = Message(role=role, content=content)

    # Then: 정상적으로 생성되고 값을 조회할 수 있다
    assert message.role == role
    assert message.content == content


def test_message_rejects_invalid_role():
    """role은 'user' 또는 'assistant'만 허용한다"""
    # When & Then: 잘못된 role이면 ValueError가 발생한다
    with pytest.raises(ValueError, match="role은 'user' 또는 'assistant'만 가능합니다"):
        Message(role="invalid", content="테스트")


def test_message_rejects_empty_content():
    """content가 빈 문자열이면 생성을 거부한다"""
    # When & Then: content가 빈 문자열이면 ValueError가 발생한다
    with pytest.raises(ValueError, match="content는 필수입니다"):
        Message(role="user", content="")


def test_message_converts_to_dict():
    """Message는 dict 형태로 변환할 수 있다"""
    # Given: Message 객체
    message = Message(role="user", content="안녕하세요")

    # When: to_dict()를 호출하면
    result = message.to_dict()

    # Then: dict 형태로 변환된다
    assert result == {"role": "user", "content": "안녕하세요"}
