from sqlalchemy import Column, Integer, String, JSON, ForeignKey
from sqlalchemy.orm import relationship

from app.database import Base


class Hotels(Base):
    __tablename__ = "hotels"

    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String, nullable=False)
    category_id = Column(ForeignKey("hotels_categories.id"), nullable=False)
    location = Column(String, nullable=False)
    services = Column(JSON, nullable=False)

    category = relationship("HotelsCategories", back_populates="hotels")
    rooms = relationship("Rooms", back_populates="hotels")


class HotelsCategories(Base):
    __tablename__ = "hotels_categories"

    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String, nullable=False)

    hotels = relationship("Hotels", back_populates="category")


class Rooms(Base):
    __tablename__ = "rooms"

    id = Column(Integer, primary_key=True, nullable=False)
    hotel_id = Column(ForeignKey("hotels.id"), nullable=False)
    name = Column(String, nullable=False)
    services = Column(JSON, nullable=False)
    price = Column(Integer, nullable=False)
    quantity = Column(Integer, nullable=False)
    quantity_left = Column(Integer, nullable=False)

    hotels = relationship("Hotels", back_populates="rooms")
