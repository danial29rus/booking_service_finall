from datetime import date, datetime
from functools import wraps

from fastapi import APIRouter, Depends, HTTPException, Form
from fastapi_cache import FastAPICache, JsonCoder
from fastapi_cache.decorator import cache
from pydantic.class_validators import Optional
from requests import Request, Response
from sqlalchemy import insert, select, update, delete
from sqlalchemy.cimmutabledict import immutabledict
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql.functions import count
from sqlalchemy.sql.expression import func
from sqlalchemy.util import asyncio

from app.api.endpoints.auth.models import Users
from app.api.endpoints.auth.utils import get_current_user
from app.api.endpoints.bookings.utils import get_booking_info
from app.database import get_async_session
from app.api.endpoints.bookings.models import Bookings
from app.api.endpoints.bookings.schemas import BookingInfo, Remove_book, Booking_room
from app.api.endpoints.hotels.models import Rooms, Hotels
from app.config import SMTP_PASSWORD, SMTP_USER
from app.api.endpoints.tasks.tasks import send_email_report_dashboard, get_email_template_dashboard

router_booking = APIRouter()





@router_booking.get("/my_bookings_v2.0")
async def get_bookings(
        current_user: Users = Depends(get_current_user),
        session: AsyncSession = Depends(get_async_session)
):
    query = select(
        Hotels.name.label("hotel_name"),
        Rooms.name.label("room_name"),
        Rooms.description.label("room_description"),
        Rooms.services.label("room_services"),
        Bookings.date_from,
        Bookings.date_to,
        Bookings.total_days,
        Bookings.total_cost,
        Rooms.image_names
    ).select_from(Bookings).filter_by(user_id=current_user.id).join(
        Rooms, Rooms.id == Bookings.room_id
    ).join(
        Hotels, Hotels.id == Rooms.hotel_id
    )
    bookings = await session.execute(query)
    bookings = bookings.all()
    bookings_json = [booking._mapping for booking in bookings]
    return bookings_json
@router_booking.post("/booking_hotel")
async def book_room(room_id: Booking_room, session: AsyncSession = Depends(get_async_session), current_user: Users = Depends(get_current_user)):
    try:
        note_dict = room_id.dict(exclude_unset=True)
        note_dict['user_id'] = current_user.id
        query_room = select(Rooms).where(room_id.room_id == Rooms.id)
        room = await session.execute(query_room)
        room = room.scalar_one()
        query_hotel = select(Hotels).where(room.hotel_id == Hotels.id)
        room_hotel = await session.execute(query_hotel)
        room_hotel = room_hotel.scalar_one()
        note_dict['price'] = room.price
        note_dict['total_cost'] = int((room_id.date_to - room_id.date_from).days) * room.price
        note_dict['total_days'] = int((room_id.date_to - room_id.date_from).days)
        note_obj = insert(Bookings).values(**note_dict)
        send_email_report_dashboard(current_user.email, room_id.date_to.strftime("%d.%m.%Y"), room_id.date_from.strftime("%d.%m.%Y"), room_hotel.name, note_dict['total_cost'])
        await session.execute(note_obj)
        await session.commit()

        return (f"{current_user.email} Вы успешно забронировали отель с {room_id.date_from} по {room_id.date_to}")

    except Exception as e:
        print(e)
        await session.rollback()
        raise HTTPException(status_code=500)


#
#
#
@router_booking.post("/remoove_booking_hotel")
async def remove_booking(room_id: int, session: AsyncSession = Depends(get_async_session), user=Depends(get_current_user)):
    delet = delete(Bookings).where(room_id == Bookings.id)

    await session.execute(delet, execution_options=immutabledict({"synchronize_session": 'fetch'}))
    await session.commit()
    return {"status": "success"}
#
#
# @router_booking.get("/my_bookings")
# @cache(expire=80)
# async def my_bookings(session: AsyncSession = Depends(get_async_session), user=Depends(get_current_user)):
#     stm = select(Rooms).where((Rooms.id == Bookings.room_id) & (Bookings.user_id == user.id))
#
#     result = await session.execute(stm, execution_options=immutabledict({"synchronize_session": 'fetch'}))
#     return result.all()

