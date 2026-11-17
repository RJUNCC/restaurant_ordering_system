from enum import Enum as PyEnum

from sqlalchemy import Column, ForeignKey, Integer, String, DECIMAL
from sqlalchemy import Enum as SqlEnum
from sqlalchemy.orm import relationship

from ..dependencies.database import Base


class PaymentType(PyEnum):
    debit = "debit"
    credit = "credit"
    cash = "cash"


class PaymentStatus(PyEnum):
    paid = "paid"
    canceled = "canceled"
    pending = "pending"


class Payment(Base):
    __tablename__ = "payments"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    order_id = Column(Integer, ForeignKey("orders.id"), nullable=False)
    type = Column(SqlEnum(PaymentType), nullable=False)
    status = Column(SqlEnum(PaymentStatus), nullable=False)
    amount = Column(DECIMAL(10, 2), nullable=False, default=0)
    # only last 4 digits are stored; null for cash
    card_number = Column(String(4), nullable=True)

    order = relationship("Order", back_populates="payments")
