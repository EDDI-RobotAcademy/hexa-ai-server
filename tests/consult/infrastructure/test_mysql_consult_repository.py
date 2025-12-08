import pytest
from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.consult.domain.consult_session import ConsultSession
from app.consult.infrastructure.model.consult_session_model import ConsultSessionModel
from app.consult.infrastructure.repository.mysql_consult_repository import MySQLConsultRepository
from app.shared.vo.mbti import MBTI
from app.shared.vo.gender import Gender
from config.database import Base


@pytest.fixture(scope="function")
def db_session():
    """테스트용 인메모리 SQLite DB 세션"""
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(bind=engine)
    SessionLocal = sessionmaker(bind=engine)
    session = SessionLocal()
    yield session
    session.close()


@pytest.fixture
def repository(db_session):
    """MySQLConsultRepository 인스턴스"""
    return MySQLConsultRepository(db_session)


def test_save_and_find_session_by_id(repository, db_session):
    """세션을 저장하고 조회할 수 있다 (영속성 검증)"""
    # Given: 유효한 ConsultSession
    session = ConsultSession(
        id="session-123",
        user_id="user-456",
        mbti=MBTI("INTJ"),
        gender=Gender("MALE"),
        created_at=datetime(2024, 1, 15, 10, 30, 0),
    )

    # When: 세션을 저장하고
    repository.save(session)

    # Then: 같은 ID로 조회하면 동일한 데이터가 반환된다
    found = repository.find_by_id("session-123")
    assert found is not None
    assert found.id == "session-123"
    assert found.user_id == "user-456"
    assert found.mbti.value == "INTJ"
    assert found.gender.value == "MALE"
    assert found.created_at == datetime(2024, 1, 15, 10, 30, 0)


def test_find_nonexistent_session_returns_none(repository):
    """존재하지 않는 세션을 조회하면 None이 반환된다"""
    # When: 존재하지 않는 세션을 조회하면
    found = repository.find_by_id("nonexistent-id")

    # Then: None이 반환된다
    assert found is None


def test_persistence_after_session_restart(db_session):
    """세션 재시작 후에도 데이터가 유지된다 (영속성 검증)"""
    # Given: 세션을 저장하고
    repository = MySQLConsultRepository(db_session)
    session = ConsultSession(
        id="session-999",
        user_id="user-888",
        mbti=MBTI("ENFP"),
        gender=Gender("FEMALE"),
    )
    repository.save(session)

    # When: 새로운 repository 인스턴스를 생성하고
    new_repository = MySQLConsultRepository(db_session)

    # Then: 저장된 데이터를 조회할 수 있다
    found = new_repository.find_by_id("session-999")
    assert found is not None
    assert found.user_id == "user-888"
    assert found.mbti.value == "ENFP"
    assert found.gender.value == "FEMALE"


def test_save_multiple_sessions(repository):
    """여러 세션을 저장하고 각각 조회할 수 있다"""
    # Given: 여러 세션을 저장하고
    session1 = ConsultSession(
        id="session-1",
        user_id="user-1",
        mbti=MBTI("INTJ"),
        gender=Gender("MALE"),
    )
    session2 = ConsultSession(
        id="session-2",
        user_id="user-2",
        mbti=MBTI("ENFP"),
        gender=Gender("FEMALE"),
    )

    repository.save(session1)
    repository.save(session2)

    # When: 각각 조회하면
    found1 = repository.find_by_id("session-1")
    found2 = repository.find_by_id("session-2")

    # Then: 각각의 데이터가 정확히 반환된다
    assert found1.user_id == "user-1"
    assert found1.mbti.value == "INTJ"
    assert found2.user_id == "user-2"
    assert found2.mbti.value == "ENFP"
