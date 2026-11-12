from sqlalchemy import Column, Integer, String, DECIMAL, DATETIME
from ..dependencies.database import Base


class Promotion(Base):
    __tablename__ = "promotions"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    promo_code = Column(String(100))
    start_date = Column(DATETIME, nullable=True)
    end_date = Column(DATETIME, nullable=True)
    discount = Column(DECIMAL(4, 2), nullable=False)