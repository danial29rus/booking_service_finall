

from sqlalchemy import Column, Integer, String, JSON, ForeignKey, Boolean
from sqlalchemy.orm import relationship

from app.database import Base

class Hotels(Base):
    __tablename__ = "hotels"

    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String, nullable=False)
    location = Column(String, nullable=False)
    services = Column(JSON, nullable=False)
    rooms_quantity = Column(Integer, nullable=False)
    image_names = Column(JSON, nullable=False)

    rooms = relationship("Rooms")


class Rooms(Base):
    __tablename__ = "rooms"

    id = Column(Integer, primary_key=True, nullable=False)
    hotel_id = Column(ForeignKey("hotels.id"), nullable=False)
    name = Column(String, nullable=False)
    description = Column(String, nullable=True)
    services = Column(JSON, nullable=True)
    price = Column(Integer, nullable=False)
    quantity = Column(Integer, nullable=False)
    image_names = Column(JSON, nullable=False)