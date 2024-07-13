from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.config.connection import db


class BaseRepository:
    def __init__(self, session: AsyncSession = Depends(db.session)):
        self._session = session
