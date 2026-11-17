from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class ResourceBase(BaseModel):
    ingredient: str
    amount: float
    unit: str

class ResourceCreate(ResourceBase):
    pass


class ResourceUpdate(BaseModel):
    ingredient: Optional[str] = None
    amount: Optional[float] = None
    unit: Optional[str] = None

class Resource(ResourceBase):
    id: int

    class ConfigDict:
        from_attributes = True
