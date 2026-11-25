from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict, Field


class ReviewBase(BaseModel):
    menu_id: Optional[int] = None
    customer_id: Optional[int] = None
    order_id: Optional[int] = None
    review_text: Optional[str] = None
    score: int = Field(ge=1, le=5)


class ReviewCreate(ReviewBase):
    pass


class ReviewUpdate(BaseModel):
    review_text: Optional[str] = None
    score: Optional[int] = Field(default=None, ge=1, le=5)


class Review(ReviewBase):
    id: int
    created_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)
