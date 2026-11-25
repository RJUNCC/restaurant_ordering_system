from sqlalchemy import Column, Integer, String, DECIMAL
from sqlalchemy.orm import relationship

from ..dependencies.database import Base


class Resource(Base):
    """An ingredient the kitchen keeps in stock."""
    __tablename__ = "resources"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    ingredient = Column(String(100), unique=True, nullable=False)
    amount = Column(DECIMAL(10, 2), nullable=False, server_default="0")
    unit = Column(String(20), nullable=False)  # e.g. g, ml, pcs, slice

    recipes = relationship("Recipe", back_populates="resource")
