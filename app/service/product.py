from fastapi import Depends, HTTPException

from app.model.product import ProductItem
from app.model.repository.product import ProductRepository


class ProductService:
    def __init__(
        self, product: ProductRepository = Depends(ProductRepository)
    ):
        self.product = product

    def _calc_discount(self, item: ProductItem):
        try:
            return 100 - int(item.price * 100 / item.cost)
        except ZeroDivisionError:
            return 0

    async def get_product_list(self):
        return [
            {
                "pk": row.Product.id,
                "name": row.Product.name,
                "price": row.min_price,
                "is_active": row.min_price is not None,
            }
            for row in await self.product.find_displayed_products()
        ]

    async def get_product(self, product_id: int):
        if not (product := await self.product.find_product(product_id)):
            raise HTTPException(status_code=404)
        items = await self.product.find_product_items_by_product(product_id)
        result = product.serialize(fields=["pk", "name"])
        result["items"] = [
            item.serialize(
                fields=[
                    "pk",
                    "name",
                    "cost",
                    "price",
                    "discount",
                    "item_quantity",
                    "sold_quantity",
                ],
                func={"discount": self._calc_discount},
            )
            for item in items
        ]
        return result
