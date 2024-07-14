from typing import Annotated

from annotated_types import Len
from pydantic import BaseModel, Field

NonBlank = Len(min_length=1)


class OrderItemInfo(BaseModel):
    item_id: int
    quantity: int = Field(gt=0)


class OrderInfo(BaseModel):
    order_number: str
    product_id: int
    items: Annotated[list[OrderItemInfo], NonBlank]
