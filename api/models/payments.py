from enum import Enum as PyEnum

from sqlalchemy import Column, Integer, String, DECIMAL, DATETIME, func
from sqlalchemy import Enum as SqlEnum
from sqlalchemy.orm import relationship

from ..dependencies.database import Base


class PaymentType(PyEnum):
    debit = "debit"
    credit = "credit"


class PaymentStatus(PyEnum):
    paid = "paid"
    canceled = "canceled"
    pending = "pending"


class Payment(Base):
    __tablename__ = "payments"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    type = Column(SqlEnum(PaymentType), nullable=False)
    status = Column(SqlEnum(PaymentStatus), nullable=False)
    amount = Column(DECIMAL(10, 2), nullable=False)
    # only last 4 digits are stored
    card_number = Column(String(4), nullable=False)
    created_at = Column(DATETIME, nullable=False, server_default=func.now())

    order = relationship("Order", back_populates="payment", uselist=False)
