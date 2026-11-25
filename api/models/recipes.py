from sqlalchemy import Column, ForeignKey, Integer, DECIMAL
from sqlalchemy.orm import relationship

from ..dependencies.database import Base


class Recipe(Base):
    """How much of each ingredient (resource) one menu item uses."""
    __tablename__ = "recipes"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    menu_id = Column(Integer, ForeignKey("menu.id"), nullable=False)
    resource_id = Column(Integer, ForeignKey("resources.id"), nullable=False)
    amount = Column(DECIMAL(10, 2), nullable=False)

    menu = relationship("Menu", back_populates="recipes")
    resource = relationship("Resource", back_populates="recipes")
