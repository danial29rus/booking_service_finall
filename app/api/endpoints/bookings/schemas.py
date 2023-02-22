from pydantic import BaseModel, json
from sqlalchemy import Date
from datetime import datetime

from pydantic.main import BaseModel

class Booking_room(BaseModel):
    room_id: int
    date_from: datetime
    date_to: datetime

class BookingInfo(BaseModel):
    hotel_name: str
    room_name: str
    room_description: str
    date_from: datetime
    date_to: datetime
    total_cost: int
    total_days: int



class Remove_book(BaseModel):
    room_id: int