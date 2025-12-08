from sqlalchemy.orm import Session

from app.consult.application.port.consult_repository_port import ConsultRepositoryPort
from app.consult.domain.consult_session import ConsultSession
from app.consult.infrastructure.model.consult_session_model import ConsultSessionModel
from app.shared.vo.mbti import MBTI
from app.shared.vo.gender import Gender


class MySQLConsultRepository(ConsultRepositoryPort):
    """MySQL 기반 상담 세션 저장소"""

    def __init__(self, db_session: Session):
        self._db = db_session

    def save(self, session: ConsultSession) -> None:
        """세션을 저장한다"""
        model = ConsultSessionModel(
            id=session.id,
            user_id=session.user_id,
            mbti=session.mbti.value,
            gender=session.gender.value,
            created_at=session.created_at,
        )
        self._db.add(model)
        self._db.commit()

    def find_by_id(self, session_id: str) -> ConsultSession | None:
        """id로 세션을 조회한다"""
        model = self._db.query(ConsultSessionModel).filter(
            ConsultSessionModel.id == session_id
        ).first()

        if model is None:
            return None

        return ConsultSession(
            id=model.id,
            user_id=model.user_id,
            mbti=MBTI(model.mbti),
            gender=Gender(model.gender),
            created_at=model.created_at,
        )
