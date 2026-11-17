from sqlalchemy import Column, Integer, String, DECIMAL
from sqlalchemy.orm import relationship

from ..dependencies.database import Base


class Sandwich(Base):
    """A menu item (dish). Table name kept from the course skeleton."""
    __tablename__ = "sandwiches"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    sandwich_name = Column(String(100), unique=True, nullable=True)
    price = Column(DECIMAL(6, 2), nullable=False, server_default='0.0')
    calories = Column(Integer, nullable=True)
    category = Column(String(50), nullable=True, index=True)  # e.g. vegetarian, kids, spicy

    recipes = relationship("Recipe", back_populates="sandwich")
    order_details = relationship("OrderDetail", back_populates="sandwich")
    reviews = relationship("Review", back_populates="sandwich")
