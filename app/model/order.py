from datetime import datetime
import enum

from sqlalchemy import (
    BigInteger,
    Column,
    DateTime,
    Enum,
    ForeignKey,
    String,
)
from sqlalchemy.orm import Mapped, relationship

from .base import BaseModel


class OrderStatus(enum.Enum):
    PENDING = "PENDING"  # 주문 대기
    COMPLETED = "COMPLETED"  # 주문 완료
    CONFIRMED = "CONFIRMED"  # 주문 확정
    CANCELLED = "CANCELLED"  # 주문 취소


class Order(BaseModel):
    __tablename__ = "tb_order"

    id = Column(BigInteger, primary_key=True)
    order_number = Column(
        String(100), comment="주문 번호", nullable=False, unique=True
    )
    product_id = Column(
        BigInteger, ForeignKey("tb_product.id", ondelete="CASCADE")
    )
    status = Column(
        Enum(OrderStatus, native_enum=False, length=10),
        comment="주문 상태",
        nullable=False,
        default=OrderStatus.PENDING
    )
    user_id = Column(
        BigInteger, ForeignKey("tb_auth_user.id", ondelete="CASCADE")
    )
    canceled_dtm = Column(
        DateTime(timezone=True), comment="주문 취소 일시", nullable=True
    )
    confirmed_dtm = Column(
        DateTime(timezone=True), comment="주문 확정 일시", nullable=True
    )
    created_dtm = Column(
        DateTime(timezone=True), nullable=False, default=datetime.utcnow
    )
    items: Mapped[list["OrderItem"]] = relationship(back_populates="order")


class OrderItem(BaseModel):
    __tablename__ = "tb_order_item"

    id = Column(BigInteger, primary_key=True)
    order_id = Column(
        BigInteger, ForeignKey("tb_order.id", ondelete="CASCADE")
    )
    item_id = Column(
        BigInteger, ForeignKey("tb_product_item.id", ondelete="CASCADE")
    )
    price = Column(BigInteger, comment="판매가", nullable=False)
    created_dtm = Column(
        DateTime(timezone=True), nullable=False, default=datetime.utcnow
    )
    order: Mapped["Order"] = relationship(back_populates="items")
