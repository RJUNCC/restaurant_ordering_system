from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class PromotionBase(BaseModel):
    promo_code: str
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    discount: float


class PromotionCreate(PromotionBase):
    pass


class PromotionUpdate(BaseModel):
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    discount: Optional[float] = None


class Promotion(PromotionBase):
    id: int

    class ConfigDict:
        from_attributes = True
