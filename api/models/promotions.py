from sqlalchemy import Column, Integer, String, DECIMAL, DATETIME
from sqlalchemy.orm import relationship

from ..dependencies.database import Base


class Promotion(Base):
    __tablename__ = "promotions"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    promo_code = Column(String(100), nullable=False, unique=True)
    start_date = Column(DATETIME, nullable=True)
    end_date = Column(DATETIME, nullable=True)  # expiration date
    discount = Column(DECIMAL(4, 2), nullable=False)

    orders = relationship("Order", back_populates="promotion")
