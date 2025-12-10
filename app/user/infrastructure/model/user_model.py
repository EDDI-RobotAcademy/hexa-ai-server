from sqlalchemy import Column, String
from config.database import Base


class UserModel(Base):
    """User ORM 모델"""

    __tablename__ = "users"

    id = Column(String(255), primary_key=True)
    email = Column(String(255), nullable=False, unique=True, index=True)
    mbti = Column(String(4), nullable=True)
    gender = Column(String(10), nullable=True)
