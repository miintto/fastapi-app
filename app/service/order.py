from fastapi import Depends, HTTPException

from app.common.security.credential import HTTPAuthorizationCredentials
from app.model.order import Order, OrderItem, OrderStatus
from app.model.repository.auth import AuthUserRepository
from app.model.repository.order import OrderRepository
from app.model.repository.order_item import OrderItemRepository
from app.model.repository.product import ProductRepository
from app.model.repository.product_item import ProductItemRepository
from app.schemas.order import OrderInfo, OrderItemInfo


class OrderService:
    def __init__(
        self,
        order: OrderRepository = Depends(OrderRepository),
        order_item: OrderItemRepository = Depends(OrderItemRepository),
        product: ProductRepository = Depends(ProductRepository),
        product_item: ProductItemRepository = Depends(ProductItemRepository),
        user: AuthUserRepository = Depends(AuthUserRepository),
    ):
        self.order = order
        self.order_item = order_item
        self.product = product
        self.product_item = product_item
        self.user = user

    async def _create_items(
        self, order: Order, items: list[OrderItemInfo]
    ) -> list[OrderItem]:
        item_map = {it.item_id: {"quantity": it.quantity} for it in items}
        await self.product.find_by_id_for_update(order.product_id)
        for item in await self.product_item.find_by_ids(item_map.keys()):
            if item.item_quantity <= item.sold_quantity:
                raise HTTPException(status_code=400, detail="Out of stock!")
            item_map[item.pk]["price"] = item.price

        item_list = [
            {"order_id": order.id, "item_id": item_id, "price": data["price"]}
            for item_id, data in item_map.items()
            for _ in range(data["quantity"])
        ]
        return await self.order_item.bulk(item_list)

    def _serialize(self, order, items):
        result = order.serialize(
            fields=[
                "pk",
                "order_number",
                "status",
                "product_id",
                "canceled_dtm",
                "confirmed_dtm",
                "created_dtm",
            ],
        )
        result["items"] = [
            item.serialize(fields=["pk", "item_id", "price"])
            for item in items
        ]
        return result

    async def create_order(
        self, data: OrderInfo, credential: HTTPAuthorizationCredentials
    ) -> dict:
        if not (product := await self.product.find_by_id(data.product_id)):
            raise HTTPException(status_code=400)
        elif not (user := await self.user.find_by_id(credential.payload.pk)):
            raise HTTPException(status_code=400)
        elif await self.order.find_by_order_number(data.order_number):
            raise HTTPException(status_code=400)

        order = await self.order.create(
            order_number=data.order_number,
            product_id=product.id,
            user_id=user.id,
        )
        items = await self._create_items(order, data.items)
        order.status = OrderStatus.COMPLETED
        await self.order.save()
        return self._serialize(order, items)

    async def search_order(self, order_id: int) -> dict:
        if not (order := await self.order.find_by_id(order_id)):
            raise HTTPException(status_code=404)
        items = await self.order_item.find_by_order_id(order_id)
        return self._serialize(order, items)
