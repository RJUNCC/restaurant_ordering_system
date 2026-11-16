from datetime import datetime
from typing import Optional
from pydantic import BaseModel
from .order_details import OrderDetail



class OrderBase(BaseModel):
    customer_id: int
    description: Optional[str] = None
    total_price = Column(DECIMAL(20, 2), nullable=False, server_default="0")
    order_type: OrderType = OrderType.TAKEOUT


class OrderCreate(OrderBase):
    pass


class OrderUpdate(BaseModel):
    customer_id: Optional[int] = None
    description: Optional[str] = None
    total_price: Optional[Decimal] = None
    order_type: Optional[OrderType] = None


class Order(OrderBase):
    id: int
    order_date: Optional[datetime] = None
    order_details: list[OrderDetail] = None

    class ConfigDict:
        from_attributes = True


class OrderType(str, Enum):
    TAKEOUT = "takeout"
    DELIVERY = "delivery"