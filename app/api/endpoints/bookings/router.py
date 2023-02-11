from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import insert, select, update, delete
from sqlalchemy.cimmutabledict import immutabledict
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql.functions import count
from sqlalchemy.sql.expression import func
from app.api.endpoints.auth.router import current_user
from app.database import get_async_session
from app.api.endpoints.bookings.models import Bookings
from app.api.endpoints.bookings.schemas import Book, Remove_book
from app.api.endpoints.hotels.models import Rooms
from app.config import SMTP_PASSWORD, SMTP_USER

router_booking = APIRouter()


@router_booking.post("/booking_hotel")
async def book_room(room_id: Book, session: AsyncSession = Depends(get_async_session), user=Depends(current_user)):
    note_dict = room_id.dict(exclude_unset=True)
    note_dict['user_id'] = user.id
    note_obj = insert(Bookings).values(**note_dict)

    up = (
        update(Rooms)
        .where(Bookings.room_id == Rooms.id)
        .values(quantity_left=Rooms.quantity_left - 1)
    )
    await session.execute(note_obj)
    await session.execute(up, execution_options=immutabledict({"synchronize_session": 'fetch'}))
    await session.commit()
    return {"status": "success"}


@router_booking.post("/remoove_booking_hotel")
async def remove_booking(room_id: int, session: AsyncSession = Depends(get_async_session), user=Depends(current_user)):
    delet = delete(Bookings).where(room_id == Bookings.room_id)
    up = (
        update(Rooms)
        .where(room_id == Rooms.id)
        .values(quantity_left=Rooms.quantity_left + 1)
    )

    await session.execute(delet, execution_options=immutabledict({"synchronize_session": 'fetch'}))
    await session.execute(up, execution_options=immutabledict({"synchronize_session": 'fetch'}))
    await session.commit()
    return {"status": "success"}

@router_booking.get("/my_bookings")
async def my_bookings(session: AsyncSession = Depends(get_async_session), user=Depends(current_user)):
    stm = select(Rooms).where((Rooms.id == Bookings.room_id) & (Bookings.user_id == user.id))

    result = await session.execute(stm, execution_options=immutabledict({"synchronize_session": 'fetch'}))
    return result.all()



