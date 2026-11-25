from datetime import datetime
from typing import Optional

from pydantic import BaseModel

from ..models.payments import PaymentStatus, PaymentType


class PaymentBase(BaseModel):
    type: PaymentType
    status: PaymentStatus
    amount: float
    card_number: str


class PaymentCreate(PaymentBase):
    pass


class PaymentUpdate(BaseModel):
    status: Optional[PaymentStatus] = None


class Payment(PaymentBase):
    id: int
    created_at: Optional[datetime] = None

    class ConfigDict:
        from_attributes = True
