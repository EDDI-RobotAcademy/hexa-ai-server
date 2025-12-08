"""
상담 세션 테이블 생성 스크립트

실행 방법:
python migrations/create_consult_sessions_table.py
"""

from config.database import engine, Base
from app.consult.infrastructure.model.consult_session_model import ConsultSessionModel


def create_tables():
    """consult_sessions 테이블 생성"""
    print("Creating consult_sessions table...")
    Base.metadata.create_all(bind=engine, tables=[ConsultSessionModel.__table__])
    print("✅ consult_sessions table created successfully!")


if __name__ == "__main__":
    create_tables()
