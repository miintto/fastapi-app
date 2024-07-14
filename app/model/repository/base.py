from fastapi import Depends
from sqlalchemy import insert, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.config.connection import db


class BaseRepository:
    model = None

    def __init__(self, session: AsyncSession = Depends(db.session)):
        self._session = session

    async def find_by_id(self, pk: int):
        result = await self._session.execute(
            select(self.model).where(self.model.id == pk)
        )
        return result.scalar_one_or_none()

    async def create(self, **kwargs):
        result = await self._session.execute(
            insert(self.model).values(kwargs).returning(self.model.id)
        )
        await self._session.commit()
        return self.model(id=result.scalar_one(), **kwargs)
