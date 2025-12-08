class Message:
    """상담 메시지 도메인 객체"""

    def __init__(self, role: str, content: str):
        """Message 객체 생성

        Args:
            role: 메시지 역할 ('user' 또는 'assistant')
            content: 메시지 내용

        Raises:
            ValueError: role이 유효하지 않거나 content가 비어있을 경우
        """
        if role not in ["user", "assistant"]:
            raise ValueError("role은 'user' 또는 'assistant'만 가능합니다")
        if not content or content == "":
            raise ValueError("content는 필수입니다")

        self._role = role
        self._content = content

    @property
    def role(self) -> str:
        """메시지 역할"""
        return self._role

    @property
    def content(self) -> str:
        """메시지 내용"""
        return self._content

    def to_dict(self) -> dict:
        """메시지를 dict 형태로 변환"""
        return {"role": self._role, "content": self._content}
