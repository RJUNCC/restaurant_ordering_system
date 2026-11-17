from datetime import datetime
from typing import Optional
from pydantic import BaseModel
from .order_details import OrderDetail
from ..models.orders import OrderStatus, OrderType


class OrderBase(BaseModel):
    customer_name: str
    description: Optional[str] = None
    customer_id: Optional[int] = None
    promotion_id: Optional[int] = None
    order_type: OrderType = OrderType.takeout


class OrderCreate(OrderBase):
    pass


class OrderUpdate(BaseModel):
    customer_name: Optional[str] = None
    description: Optional[str] = None
    status: Optional[OrderStatus] = None
    promotion_id: Optional[int] = None


class Order(OrderBase):
    id: int
    order_date: Optional[datetime] = None
    tracking_number: Optional[str] = None
    status: Optional[OrderStatus] = None
    total_price: Optional[float] = None
    order_details: list[OrderDetail] = None

    class ConfigDict:
        from_attributes = True
