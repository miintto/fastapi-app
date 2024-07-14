from datetime import datetime, timezone

from sqlalchemy import select, update

from app.model.order import Order, OrderStatus
from .base import BaseRepository


class OrderRepository(BaseRepository):
    model = Order

    async def find_by_order_number(self, order_number: str) -> Order | None:
        result = await self._session.execute(
            select(Order).where(Order.order_number == order_number)
        )
        return result.scalar_one_or_none()

    async def update_status(self, pk: int, status: OrderStatus):
        await self._session.execute(
            update(Order)
            .values(status=status, updated_dtm=datetime.now(timezone.utc))
            .where(Order.id == pk)
        )
        await self._session.commit()
