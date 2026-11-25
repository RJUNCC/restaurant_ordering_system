from typing import Optional
from pydantic import BaseModel


class MenuBase(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    calories: Optional[int] = None
    category: Optional[str] = None


class MenuCreate(MenuBase):
    pass


class MenuUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    calories: Optional[int] = None
    category: Optional[str] = None


class Menu(MenuBase):
    id: int

    class ConfigDict:
        from_attributes = True
