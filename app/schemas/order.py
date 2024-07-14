from pydantic import BaseModel


class OrderItemInfo(BaseModel):
    item_id: int
    quantity: int


class OrderInfo(BaseModel):
    order_number: str
    product_id: int
    items: list[OrderItemInfo]
