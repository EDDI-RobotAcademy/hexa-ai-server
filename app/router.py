"""
Centralized router configuration.
All application routers are registered here and imported into main.py.
"""

from fastapi import FastAPI

from app.auth.adapter.input.web.oauth_router import oauth_router
from app.data.adapter.input.web.data_router import data_router
from app.data.infrastructure.orm.data_orm import DataORM  # noqa: F401
from app.consult.infrastructure.orm.consult_orm import ConsultORM  # noqa: F401


def setup_routers(app: FastAPI) -> None:
    app.include_router(oauth_router, prefix="/auth")
    app.include_router(data_router, prefix="/data")
