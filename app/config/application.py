from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError

from app.config.connection import db
from app.router import router
from .exception_handlers import (
    request_validation_exception_error_handler,
    server_exception_handler,
)


def create_app() -> FastAPI:
    app = FastAPI(
        docs_url=None,
        redoc_url="/documents",
        exception_handlers={
            RequestValidationError: request_validation_exception_error_handler,
            Exception: server_exception_handler,
        },
    )
    app.include_router(router)

    # Databases
    app.add_event_handler("startup", db.check_connection)
    app.add_event_handler("shutdown", db.dispose_connection)

    return app
