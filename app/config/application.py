from fastapi import FastAPI

from app.config.connection import db
from app.router import router


def create_app() -> FastAPI:
    app = FastAPI(
        docs_url=None,
        redoc_url="/documents",
    )
    app.include_router(router)

    # Databases
    app.add_event_handler("startup", db.check_connection)
    app.add_event_handler("shutdown", db.dispose_connection)

    return app
