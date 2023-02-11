from pydantic import BaseModel, json
from sqlalchemy import Date
from datetime import datetime

class Book(BaseModel):
    room_id: int
    date_from: datetime
    date_to: datetime

class Remove_book(BaseModel):
    room_id: int