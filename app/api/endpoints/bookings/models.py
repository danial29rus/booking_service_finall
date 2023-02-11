from sqlalchemy import Column, Integer, ForeignKey, Date
from sqlalchemy.orm import relationship

from app.database import Base


class Bookings(Base):
    __tablename__ = "bookings"

    id = Column(Integer, primary_key=True)
    room_id = Column(ForeignKey("rooms.id"))
    user_id = Column(ForeignKey("users.id"))
    date_from = Column(Date)
    date_to = Column(Date)

    users = relationship("Users", back_populates="...")
    rooms = relationship("Rooms", back_populates="...")