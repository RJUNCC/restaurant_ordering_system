from sqlalchemy import Column, ForeignKey, Integer, String, DATETIME, CheckConstraint
from sqlalchemy.orm import relationship
from datetime import datetime

from ..dependencies.database import Base


class Review(Base):
    __tablename__ = "reviews"
    __table_args__ = (CheckConstraint("score BETWEEN 1 AND 5", name="ck_reviews_score_range"),)

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    customer_id = Column(Integer, ForeignKey("customers.id"), nullable=True)
    sandwich_id = Column(Integer, ForeignKey("sandwiches.id"), nullable=False)
    review_text = Column(String(500), nullable=True)
    score = Column(Integer, nullable=False)
    created_at = Column(DATETIME, nullable=False, default=datetime.now)

    customer = relationship("Customer", back_populates="reviews")
    sandwich = relationship("Sandwich", back_populates="reviews")
