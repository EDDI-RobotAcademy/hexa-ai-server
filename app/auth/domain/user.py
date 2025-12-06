class User:
    """User 도메인 엔티티"""

    def __init__(self, id: str, email: str):
        self._validate(id, email)
        self.id = id
        self.email = email

    def _validate(self, id: str, email: str) -> None:
        """User 값의 유효성을 검증한다"""
        if not id:
            raise ValueError("User id는 비어있을 수 없습니다")
        if not email:
            raise ValueError("User email은 비어있을 수 없습니다")