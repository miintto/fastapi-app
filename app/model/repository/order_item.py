from sqlalchemy import insert, select

from app.model.order import OrderItem
from .base import BaseRepository


class OrderItemRepository(BaseRepository):
    model = OrderItem

    async def bulk(self, *args):
        result = await self._session.execute(
            insert(OrderItem).values(*args).returning(OrderItem.id)
        )
        await self._session.commit()
        return [OrderItem(id=pk, **item) for pk, item in zip(result.scalars(), *args)]

    async def find_by_order_id(self, order_id: int):
        result = await self._session.execute(
            select(OrderItem).where(OrderItem.order_id == order_id)
        )
        return result.scalars()
