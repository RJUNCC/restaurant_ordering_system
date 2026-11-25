import uuid
from enum import Enum as PyEnum

from sqlalchemy import Column, ForeignKey, Integer, String, DECIMAL, DATETIME, func
from sqlalchemy import Enum as SqlEnum
from sqlalchemy.orm import relationship

from ..dependencies.database import Base


class OrderStatus(PyEnum):
    pending = "pending"
    preparing = "preparing"
    ready = "ready"
    delivered = "delivered"
    canceled = "canceled"


class OrderType(PyEnum):
    takeout = "takeout"
    delivery = "delivery"


def generate_tracking_number():
    return uuid.uuid4().hex[:10].upper()


class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    customer_id = Column(Integer, ForeignKey("customers.id"), nullable=False)
    promotion_id = Column(Integer, ForeignKey("promotions.id"), nullable=True)
    payment_id = Column(Integer, ForeignKey("payments.id"), nullable=True, unique=True)
    order_date = Column(DATETIME, nullable=False, server_default=func.now(), index=True)
    tracking_number = Column(String(20), unique=True, nullable=False, default=generate_tracking_number)
    status = Column(SqlEnum(OrderStatus), nullable=False, default=OrderStatus.pending)
    order_type = Column(SqlEnum(OrderType), nullable=False, default=OrderType.takeout)
    total_price = Column(DECIMAL(10, 2), nullable=False, server_default="0")
    description = Column(String(300))

    customer = relationship("Customer", back_populates="orders")
    promotion = relationship("Promotion", back_populates="orders")
    payment = relationship("Payment", back_populates="order")
    order_details = relationship("OrderDetail", back_populates="order")
