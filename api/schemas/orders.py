from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field
from .order_details import OrderDetail
from ..models.orders import OrderStatus, OrderType


class OrderBase(BaseModel):
    customer_id: int
    order_type: OrderType = OrderType.takeout
    promotion_id: Optional[int] = None
    payment_id: Optional[int] = None
    description: Optional[str] = None


class OrderCreate(OrderBase):
    pass


class OrderUpdate(BaseModel):
    customer_id: Optional[int] = None
    order_type: Optional[OrderType] = None
    status: Optional[OrderStatus] = None
    promotion_id: Optional[int] = None
    payment_id: Optional[int] = None
    total_price: Optional[float] = None
    description: Optional[str] = None


class Order(OrderBase):
    id: int
    order_date: Optional[datetime] = None
    tracking_number: Optional[str] = None
    status: Optional[OrderStatus] = None
    total_price: Optional[float] = None
    order_details: list[OrderDetail] = None

    class ConfigDict:
        from_attributes = True

class CheckoutItem(BaseModel):
    menu_id: int
    amount: int = Field(ge=1)

class GuestCheckout(BaseModel):
    name: str
    phone: str
    address: str 
    email: Optional[str]= None
    order_type: OrderType
    items: list[CheckoutItem] = Field(min_length=1)
    description: Optional[str] = None 
    promo_code: Optional[str] = None
