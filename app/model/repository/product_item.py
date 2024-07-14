from typing import Iterable

from sqlalchemy import ScalarResult, select

from app.model.product import ProductItem
from .base import BaseRepository


class ProductItemRepository(BaseRepository):
    model = ProductItem

    async def find_by_ids(
        self, pk_list: Iterable[int]
    ) -> ScalarResult[ProductItem]:
        result = await self._session.execute(
            select(ProductItem).where(ProductItem.id.in_(pk_list))
        )
        return result.scalars()

    async def find_by_product_id(
        self, product_id: int
    ) -> ScalarResult[ProductItem]:
        result = await self._session.execute(
            select(ProductItem)
            .where(
                ProductItem.product_id == product_id,
                ProductItem.is_active.is_(True),
            )
        )
        return result.scalars()
