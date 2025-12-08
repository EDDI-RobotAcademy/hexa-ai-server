from abc import ABC, abstractmethod
from typing import Optional

from app.convert.domain.consult_session import ConsultSession


class ConsultRepositoryPort(ABC):
    """상담 세션 저장소 포트 인터페이스"""

    @abstractmethod
    def save(self, session: ConsultSession) -> ConsultSession:
        """세션을 저장하고 저장된 세션을 반환

        Args:
            session: 저장할 세션

        Returns:
            저장된 세션
        """
        raise NotImplementedError

    @abstractmethod
    def find_by_id(self, session_id: str) -> Optional[ConsultSession]:
        """세션 ID로 세션을 조회

        Args:
            session_id: 조회할 세션 ID

        Returns:
            찾은 세션 또는 None
        """
        raise NotImplementedError
