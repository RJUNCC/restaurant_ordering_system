from enum import Enum as PyEnum
from datetime import datetime

from sqlalchemy import Column, ForeignKey, Integer, String, DECIMAL, DATETIME
from sqlalchemy import Enum as SqlEnum
from sqlalchemy.orm import relationship

from ..dependencies.database import Base


class OrderStatus(PyEnum):
    pending = "pending"
    preparing = "preparing"
    ready = "ready"
    out_for_delivery = "out_for_delivery"
    completed = "completed"
    canceled = "canceled"


class OrderType(PyEnum):
    takeout = "takeout"
    delivery = "delivery"


class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    # nullable so guests can order without an account
    customer_id = Column(Integer, ForeignKey("customers.id"), nullable=True)
    promotion_id = Column(Integer, ForeignKey("promotions.id"), nullable=True)
    customer_name = Column(String(100))
    order_date = Column(DATETIME, nullable=False, default=datetime.now)
    tracking_number = Column(String(50), unique=True, nullable=True, index=True)
    status = Column(SqlEnum(OrderStatus), nullable=False, default=OrderStatus.pending)
    order_type = Column(SqlEnum(OrderType), nullable=False, default=OrderType.takeout)
    total_price = Column(DECIMAL(10, 2), nullable=False, default=0)
    description = Column(String(300))

    customer = relationship("Customer", back_populates="orders")
    promotion = relationship("Promotion", back_populates="orders")
    order_details = relationship("OrderDetail", back_populates="order", cascade="all, delete-orphan")
    payments = relationship("Payment", back_populates="order")
