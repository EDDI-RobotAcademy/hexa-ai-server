import pytest
from app.convert.domain.consult_session import ConsultSession
from app.convert.domain.message import Message
from app.shared.domain.user_profile import UserProfile
from app.shared.domain.gender import Gender
from app.shared.domain.mbti import MBTI


def test_consult_session_creates_with_user_id_and_profile():
    """ConsultSession은 user_id와 profile로 생성된다"""
    # Given: user_id와 profile
    user_id = "user-123"
    profile = UserProfile(gender=Gender("FEMALE"), mbti=MBTI("INTJ"))

    # When: ConsultSession 객체를 생성하면
    session = ConsultSession(user_id=user_id, profile=profile)

    # Then: 정상적으로 생성되고 값을 조회할 수 있다
    assert session.user_id == user_id
    assert session.profile == profile
    assert session.session_id is not None  # UUID 자동 생성


def test_consult_session_adds_message():
    """ConsultSession은 메시지를 추가할 수 있다"""
    # Given: ConsultSession 객체
    user_id = "user-123"
    profile = UserProfile(gender=Gender("MALE"), mbti=MBTI("ENFP"))
    session = ConsultSession(user_id=user_id, profile=profile)

    # When: 메시지를 추가하면
    message = Message(role="user", content="안녕하세요")
    session.add_message(message)

    # Then: 메시지가 저장된다
    messages = session.get_messages()
    assert len(messages) == 1
    assert messages[0] == message


def test_consult_session_counts_user_turns():
    """ConsultSession은 사용자 턴 수를 카운트할 수 있다"""
    # Given: ConsultSession에 여러 메시지 추가
    session = ConsultSession(
        user_id="user-123",
        profile=UserProfile(gender=Gender("MALE"), mbti=MBTI("ENFP"))
    )
    session.add_message(Message(role="user", content="첫 번째 질문"))
    session.add_message(Message(role="assistant", content="답변1"))
    session.add_message(Message(role="user", content="두 번째 질문"))
    session.add_message(Message(role="assistant", content="답변2"))
    session.add_message(Message(role="user", content="세 번째 질문"))

    # When: get_user_turn_count()를 호출하면
    turn_count = session.get_user_turn_count()

    # Then: user 역할 메시지 개수가 반환된다
    assert turn_count == 3


def test_consult_session_checks_completion():
    """ConsultSession은 3턴 완료 여부를 확인할 수 있다"""
    # Given: ConsultSession
    session = ConsultSession(
        user_id="user-123",
        profile=UserProfile(gender=Gender("MALE"), mbti=MBTI("ENFP"))
    )

    # When: 3턴 미만일 때
    session.add_message(Message(role="user", content="질문1"))
    session.add_message(Message(role="assistant", content="답변1"))

    # Then: is_completed()가 False
    assert session.is_completed() is False

    # When: 3턴 완료했을 때
    session.add_message(Message(role="user", content="질문2"))
    session.add_message(Message(role="assistant", content="답변2"))
    session.add_message(Message(role="user", content="질문3"))
    session.add_message(Message(role="assistant", content="답변3"))

    # Then: is_completed()가 True
    assert session.is_completed() is True


def test_consult_session_gets_conversation_history():
    """ConsultSession은 대화 내역을 dict 리스트로 반환할 수 있다"""
    # Given: 메시지가 있는 ConsultSession
    session = ConsultSession(
        user_id="user-123",
        profile=UserProfile(gender=Gender("MALE"), mbti=MBTI("ENFP"))
    )
    session.add_message(Message(role="user", content="안녕하세요"))
    session.add_message(Message(role="assistant", content="반갑습니다"))

    # When: get_conversation_history()를 호출하면
    history = session.get_conversation_history()

    # Then: dict 리스트 형태로 반환된다
    assert history == [
        {"role": "user", "content": "안녕하세요"},
        {"role": "assistant", "content": "반갑습니다"}
    ]
