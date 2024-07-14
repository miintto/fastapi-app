from typing import Sequence

from fastapi import Depends
from sqlalchemy import insert, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.config.connection import db


class BaseRepository:
    model = None

    def __init__(self, session: AsyncSession = Depends(db.session)):
        self._session = session

    async def save(self):
        await self._session.commit()

    async def create(self, **kwargs):
        result = await self._session.execute(
            insert(self.model).values(kwargs).returning(self.model)
        )
        await self._session.commit()
        return result.scalar_one()

    async def find_by_id(self, pk: int, entities: Sequence = None):
        if not entities:
            entities = (self.model,)
        result = await self._session.execute(
            select(*entities).where(self.model.id == pk)
        )
        return result.scalar_one_or_none()
