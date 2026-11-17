from typing import Optional

from pydantic import BaseModel

from ..models.payments import PaymentStatus, PaymentType


class PaymentBase(BaseModel):
    order_id: int
    type: PaymentType
    status: PaymentStatus
    amount: float
    card_number: Optional[str] = None  # last 4 digits only


class PaymentCreate(PaymentBase):
    pass


class PaymentUpdate(BaseModel):
    status: Optional[PaymentStatus] = None


class Payment(PaymentBase):
    id: int

    class ConfigDict:
        from_attributes = True
