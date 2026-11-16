from enum import Enum as PyEnum

from sqlalchemy import VARCHAR, Column, Integer
from sqlalchemy import Enum as SqlEnum

from ..dependencies.database import Base


class PaymentType(PyEnum):
    debit = "debit"
    credit = "credit"
    gift_card = "gift_card"


class PaymentStatus(PyEnum):
    paid = "paid"
    canceled = "canceled"
    pending = "pending"


class Payment(Base):
    __tablename__ = "payments"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    type = Column(SqlEnum(PaymentType), nullable=False)
    status = Column(SqlEnum(PaymentStatus), nullable=False)
    card_number = Column(VARCHAR, nullable=False)
