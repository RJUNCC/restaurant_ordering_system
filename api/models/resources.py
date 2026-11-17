from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from ..dependencies.database import Base


class Resource(Base):
    """An ingredient / stock item the kitchen tracks."""
    __tablename__ = "resources"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    item = Column(String(100), unique=True, nullable=False)
    amount = Column(Integer, index=True, nullable=False, server_default='0')
    unit = Column(String(20), nullable=False, server_default='unit')  # e.g. g, oz, slices

    recipes = relationship("Recipe", back_populates="resource")
