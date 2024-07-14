from datetime import datetime, timezone

from sqlalchemy import Row,  func, select

from app.model.product import Product, ProductItem
from .base import BaseRepository


class ProductRepository(BaseRepository):
    model = Product

    async def find_displayed_products(self) -> list[Row[tuple[Product, int]]]:
        result = await self._session.execute(
            select(
                Product,
                (
                    select(func.min(ProductItem.price))
                    .where(
                        ProductItem.sale_start_dtm.is_(None)
                        | (ProductItem.sale_start_dtm < datetime.now(timezone.utc)),
                        ProductItem.sale_close_dtm.is_(None)
                        | (ProductItem.sale_close_dtm > datetime.now(timezone.utc)),
                        ProductItem.product_id == Product.id,
                        ProductItem.is_active.is_(True),
                        ProductItem.sold_quantity < ProductItem.item_quantity,
                    )
                    .scalar_subquery()
                    .label("min_price")
                ),
            )
            .where(Product.is_displayed.is_(True))
        )
        return result.fetchall()
