from sqlalchemy import Column, Integer, String, DECIMAL
from sqlalchemy.orm import relationship

from ..dependencies.database import Base


class Menu(Base):
    """A menu item (dish)."""
    __tablename__ = "menu"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(100), unique=True, nullable=False)
    description = Column(String(300), nullable=True)
    price = Column(DECIMAL(6, 2), nullable=False, server_default="0")
    calories = Column(Integer, nullable=True)
    category = Column(String(50), nullable=True, index=True)  # e.g. vegetarian, kids, spicy

    recipes = relationship("Recipe", back_populates="menu")
    order_details = relationship("OrderDetail", back_populates="menu")
    reviews = relationship("Review", back_populates="menu")
