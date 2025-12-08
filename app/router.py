"""
Centralized router configuration.
All application routers are registered here and imported into main.py.
"""

from fastapi import FastAPI

from app.auth.adapter.input.web.google_oauth_router import google_oauth_router
from app.data.adapter.input.web.data_router import data_router
from app.data.infrastructure.orm.data_orm import DataORM  # noqa: F401
from app.convert.infrastructure.orm.consult_orm import ConsultORM  # noqa: F401
from app.convert.adapter.input.web.consult_router import consult_router
from app.consult.adapter.input.web import consult_router as consult_router_module
from app.user.application.port.user_repository_port import UserRepositoryPort
from tests.user.fixtures.fake_user_repository import FakeUserRepository
from tests.consult.fixtures.fake_consult_repository import FakeConsultRepository


def setup_routers(app: FastAPI) -> None:
    # Auth router
    app.include_router(google_oauth_router, prefix="/auth")

    # Data router
    app.include_router(data_router, prefix="/data")
    app.include_router(consult_router, prefix="/convert")

    # Consult router with dependency injection
    # TODO: Replace with real repository implementation
    consult_router_module._user_repository = FakeUserRepository()
    consult_router_module._consult_repository = FakeConsultRepository()
    app.include_router(consult_router, prefix="/consult")