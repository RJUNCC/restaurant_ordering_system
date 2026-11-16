from typing import Optional

from pydantic import BaseModel

from ..models.payments import PaymentStatus, PaymentType


class PaymentBase(BaseModel):
    type: PaymentType
    status: PaymentStatus
    card_number: str


class PaymentCreate(PaymentBase):
    pass


class PaymentUpdate(BaseModel):
    status: Optional[PaymentStatus]


class Payment(PaymentBase):
    id: int

    class ConfigDict:
        from_attributes = True
