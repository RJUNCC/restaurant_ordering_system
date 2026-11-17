from sqlalchemy import Column, ForeignKey, Integer, UniqueConstraint
from sqlalchemy.orm import relationship

from ..dependencies.database import Base


class Recipe(Base):
    """Join table: how much of each resource one menu item uses."""
    __tablename__ = "recipes"
    __table_args__ = (UniqueConstraint("sandwich_id", "resource_id", name="uq_recipe_item_resource"),)

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    sandwich_id = Column(Integer, ForeignKey("sandwiches.id"), nullable=False)
    resource_id = Column(Integer, ForeignKey("resources.id"), nullable=False)
    amount = Column(Integer, index=True, nullable=False, server_default='0')

    sandwich = relationship("Sandwich", back_populates="recipes")
    resource = relationship("Resource", back_populates="recipes")
