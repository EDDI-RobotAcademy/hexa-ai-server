from sqlalchemy import Column, String, DateTime
from config.database import Base


class ConsultSessionModel(Base):
    """상담 세션 ORM 모델"""

    __tablename__ = "consult_sessions"

    id = Column(String(36), primary_key=True)
    user_id = Column(String(255), nullable=False, index=True)
    mbti = Column(String(4), nullable=False)
    gender = Column(String(10), nullable=False)
    created_at = Column(DateTime, nullable=False)
