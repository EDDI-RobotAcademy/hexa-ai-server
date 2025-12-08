import uuid
from app.convert.domain.message import Message
from app.shared.domain.user_profile import UserProfile


class ConsultSession:
    """상담 세션 도메인 객체"""

    def __init__(self, user_id: str, profile: UserProfile, session_id: str = None):
        """ConsultSession 객체 생성

        Args:
            user_id: 사용자 ID
            profile: 사용자 프로필 (MBTI, Gender)
            session_id: 세션 ID (없으면 자동 생성)
        """
        self._session_id = session_id or str(uuid.uuid4())
        self._user_id = user_id
        self._profile = profile
        self._messages: list[Message] = []

    @property
    def session_id(self) -> str:
        """세션 ID"""
        return self._session_id

    @property
    def user_id(self) -> str:
        """사용자 ID"""
        return self._user_id

    @property
    def profile(self) -> UserProfile:
        """사용자 프로필"""
        return self._profile

    def add_message(self, message: Message) -> None:
        """메시지를 세션에 추가

        Args:
            message: 추가할 메시지
        """
        self._messages.append(message)

    def get_messages(self) -> list[Message]:
        """세션의 모든 메시지 조회

        Returns:
            메시지 리스트
        """
        return self._messages.copy()

    def get_user_turn_count(self) -> int:
        """사용자 턴 수 카운트

        Returns:
            user 역할 메시지 개수
        """
        return sum(1 for msg in self._messages if msg.role == "user")

    def is_completed(self) -> bool:
        """상담 완료 여부 확인 (3턴 완료)

        Returns:
            3턴 이상 완료했으면 True
        """
        return self.get_user_turn_count() >= 3

    def get_conversation_history(self) -> list[dict]:
        """대화 내역을 dict 리스트로 반환

        Returns:
            [{"role": "user", "content": "..."}, ...] 형태의 리스트
        """
        return [msg.to_dict() for msg in self._messages]
