from sqlalchemy import Column, ForeignKey, Integer, CheckConstraint
from sqlalchemy.orm import relationship

from ..dependencies.database import Base


class OrderDetail(Base):
    __tablename__ = "order_details"
    __table_args__ = (CheckConstraint("amount > 0", name="ck_order_details_amount_positive"),)

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    order_id = Column(Integer, ForeignKey("orders.id"), nullable=False)
    sandwich_id = Column(Integer, ForeignKey("sandwiches.id"), nullable=False)
    amount = Column(Integer, index=True, nullable=False)

    sandwich = relationship("Sandwich", back_populates="order_details")
    order = relationship("Order", back_populates="order_details")
