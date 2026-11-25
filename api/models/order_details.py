from sqlalchemy import Column, ForeignKey, Integer
from sqlalchemy.orm import relationship

from ..dependencies.database import Base


class OrderDetail(Base):
    __tablename__ = "order_details"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    order_id = Column(Integer, ForeignKey("orders.id"), nullable=False)
    menu_id = Column(Integer, ForeignKey("menu.id"), nullable=False)
    amount = Column(Integer, nullable=False)

    menu = relationship("Menu", back_populates="order_details")
    order = relationship("Order", back_populates="order_details")
