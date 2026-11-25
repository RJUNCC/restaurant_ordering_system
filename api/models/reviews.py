from sqlalchemy import Column, ForeignKey, Integer, String, DATETIME, CheckConstraint, func
from sqlalchemy.orm import relationship

from ..dependencies.database import Base


class Review(Base):
    __tablename__ = "reviews"
    __table_args__ = (CheckConstraint("score BETWEEN 1 AND 5", name="ck_reviews_score_range"),)

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    customer_id = Column(Integer, ForeignKey("customers.id"), nullable=True)
    menu_id = Column(Integer, ForeignKey("menu.id"), nullable=True)
    order_id = Column(Integer, ForeignKey("orders.id"), nullable=True)
    review_text = Column(String(500), nullable=True)
    score = Column(Integer, nullable=False)
    created_at = Column(DATETIME, nullable=False, server_default=func.now())

    customer = relationship("Customer", back_populates="reviews")
    menu = relationship("Menu", back_populates="reviews")
    order = relationship("Order")
