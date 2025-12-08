import pytest
from datetime import datetime
from app.consult.domain.consult_session import ConsultSession
from app.shared.vo.mbti import MBTI
from app.shared.vo.gender import Gender


def test_consult_session_creates_with_required_fields():
    """필수 필드로 ConsultSession 객체를 생성할 수 있다"""
    # Given: 유효한 세션 정보
    session_id = "session-uuid-123"
    user_id = "user-456"
    mbti = MBTI("INTJ")
    gender = Gender("MALE")

    # When: ConsultSession 객체를 생성하면
    session = ConsultSession(
        id=session_id,
        user_id=user_id,
        mbti=mbti,
        gender=gender
    )

    # Then: 정상적으로 생성되고 값을 조회할 수 있다
    assert session.id == session_id
    assert session.user_id == user_id
    assert session.mbti.value == "INTJ"
    assert session.gender.value == "MALE"
    assert isinstance(session.created_at, datetime)


def test_consult_session_rejects_empty_id():
    """빈 id를 거부한다"""
    # Given: 빈 session_id
    session_id = ""
    user_id = "user-456"
    mbti = MBTI("INTJ")
    gender = Gender("MALE")

    # When & Then: ConsultSession 생성 시 ValueError가 발생한다
    with pytest.raises(ValueError):
        ConsultSession(id=session_id, user_id=user_id, mbti=mbti, gender=gender)


def test_consult_session_rejects_empty_user_id():
    """빈 user_id를 거부한다"""
    # Given: 빈 user_id
    session_id = "session-123"
    user_id = ""
    mbti = MBTI("INTJ")
    gender = Gender("MALE")

    # When & Then: ConsultSession 생성 시 ValueError가 발생한다
    with pytest.raises(ValueError):
        ConsultSession(id=session_id, user_id=user_id, mbti=mbti, gender=gender)


def test_consult_session_rejects_none_mbti():
    """None인 mbti를 거부한다"""
    # Given: None인 mbti
    session_id = "session-123"
    user_id = "user-456"
    mbti = None
    gender = Gender("MALE")

    # When & Then: ConsultSession 생성 시 ValueError가 발생한다
    with pytest.raises(ValueError):
        ConsultSession(id=session_id, user_id=user_id, mbti=mbti, gender=gender)


def test_consult_session_rejects_none_gender():
    """None인 gender를 거부한다"""
    # Given: None인 gender
    session_id = "session-123"
    user_id = "user-456"
    mbti = MBTI("INTJ")
    gender = None

    # When & Then: ConsultSession 생성 시 ValueError가 발생한다
    with pytest.raises(ValueError):
        ConsultSession(id=session_id, user_id=user_id, mbti=mbti, gender=gender)


def test_consult_session_add_message():
    """세션에 메시지를 추가할 수 있다"""
    from app.consult.domain.message import Message

    # Given: ConsultSession
    session = ConsultSession(
        id="session-123",
        user_id="user-456",
        mbti=MBTI("INTJ"),
        gender=Gender("MALE")
    )

    # When: 메시지를 추가하면
    session.add_message(Message(role="user", content="안녕하세요"))

    # Then: 메시지가 저장된다
    messages = session.get_messages()
    assert len(messages) == 1
    assert messages[0].role == "user"
    assert messages[0].content == "안녕하세요"


def test_consult_session_get_messages_returns_empty_list_initially():
    """새 세션의 메시지 목록은 비어있다"""
    # Given: 새로운 ConsultSession
    session = ConsultSession(
        id="session-123",
        user_id="user-456",
        mbti=MBTI("INTJ"),
        gender=Gender("MALE")
    )

    # When & Then: 메시지 목록이 비어있다
    assert session.get_messages() == []


def test_consult_session_messages_maintain_order():
    """메시지는 추가된 순서를 유지한다"""
    from app.consult.domain.message import Message

    # Given: ConsultSession
    session = ConsultSession(
        id="session-123",
        user_id="user-456",
        mbti=MBTI("INTJ"),
        gender=Gender("MALE")
    )

    # When: 여러 메시지를 추가하면
    session.add_message(Message(role="user", content="첫 번째"))
    session.add_message(Message(role="assistant", content="두 번째"))
    session.add_message(Message(role="user", content="세 번째"))

    # Then: 순서가 유지된다
    messages = session.get_messages()
    assert len(messages) == 3
    assert messages[0].content == "첫 번째"
    assert messages[1].content == "두 번째"
    assert messages[2].content == "세 번째"
