from typing import Optional
from pydantic import BaseModel
from .resources import Resource
from .menu import Menu


class RecipeBase(BaseModel):
    amount: float


class RecipeCreate(RecipeBase):
    menu_id: int
    resource_id: int


class RecipeUpdate(BaseModel):
    menu_id: Optional[int] = None
    resource_id: Optional[int] = None
    amount: Optional[float] = None


class Recipe(RecipeBase):
    id: int
    menu: Menu = None
    resource: Resource = None

    class ConfigDict:
        from_attributes = True
