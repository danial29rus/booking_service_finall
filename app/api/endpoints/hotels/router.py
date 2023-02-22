from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_async_session
from app.api.endpoints.hotels.models import Hotels, Rooms
from datetime import date, datetime

from fastapi import APIRouter, Depends, Query
from fastapi.encoders import jsonable_encoder
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_, or_, func

from app.api.endpoints.bookings.models import Bookings
from app.api.endpoints.hotels.models import Hotels, Rooms
from app.database import get_async_session

router = APIRouter(
    prefix="/hotels",
    tags=["hotels"]
)


@router.get("/location")
async def get_hotel_locations(location_hotel: str, session: AsyncSession = Depends(get_async_session)):
    try:
        query = select(Hotels).where(Hotels.location.contains(location_hotel.title()))
        result = await session.execute(query)
        return {
            "status": "success",
            "data": result.all(),
            "details": None
        }
    except Exception as e:
        print(e)
        return {
            'status': 'error',
            'data': None,
            'details': None
        }


# @router.get("/id")
# async def get_id_room(session: AsyncSession = Depends(get_async_session)):
#     try:
#         query = select(Rooms).where(Rooms.quantity_left > 1)
#         result = await session.execute(query)
#         return result.all()
#     except:
#         return {
#             'status': 'error',
#             'data': None,
#             'details': None
#         }




@router.get("get_hotalsV2.0")
async def get_hotels_by_location_and_time_v2_0(
        location: str,
        date_from: date = Query(..., description=f"Например, {datetime.now().date()}"),
        date_to: date = Query(..., description=f"Например, {datetime.now().date()}"),
        session: AsyncSession = Depends(get_async_session)):
    try:
        # '''select hotels.id from hotels
        # left Join rooms ON rooms.hotel_id = hotels.id
        # left join (
        # select * from bookings
        # WHERE (date_from < '2023-02-15'  AND date_to > '2023-02-15')) as book
        # ON book.room_id = rooms.id
        # WHERE (hotels.location LIKE '%' || 'Алтай' || '%')'''
        # book = select(Bookings).filter(or_(
        #     and_(
        #         Bookings.date_from < date_from,
        #         Bookings.date_to > date_from
        #     ),
        #     and_(
        #         Bookings.date_from >= date_from,
        #         Bookings.date_from < date_to
        #     )
        # )).subquery('filtered_bookings')
        #
        # hotels = select([Hotels.c.id]).select_from(Hotels).outerjoin(Rooms, Rooms.c.hotel_id == Hotels.c.id).outerjoin(
        # book, book.c.room_id == Rooms.c.id).where(
        # Hotels.location.contains(location.title()))
        #
        # hotels_info = await session.execute(book)
        bookings_for_selected_dates = select(Bookings).filter(or_(
            and_(
                Bookings.date_from < date_from,
                Bookings.date_to > date_from
            ),
            and_(
                Bookings.date_from >= date_from,
                Bookings.date_from < date_to
            )
        )).subquery('filtered_bookings')

        hotels_rooms_left = select(
            (Hotels.rooms_quantity - func.count(bookings_for_selected_dates.c.room_id)).label("rooms_left"),
            Rooms.hotel_id
        ).select_from(Hotels).outerjoin(
            Rooms, Rooms.hotel_id == Hotels.id
        ).outerjoin(
            bookings_for_selected_dates, bookings_for_selected_dates.c.room_id == Rooms.id
        ).where(
            Hotels.location.contains(location.title()),
        ).group_by(Hotels.rooms_quantity, Rooms.hotel_id).cte('hotels_rooms_left')

        get_hotels_info = select('*').select_from(Hotels).join(
            hotels_rooms_left, hotels_rooms_left.c.hotel_id == Hotels.id
        ).where(hotels_rooms_left.c.rooms_left > 0)

        hotels_info = await session.execute(get_hotels_info)


        return {
            "status": "success",
            "data": hotels_info.all(),
            "details": None
        }

    except Exception as e:
        print(e)
        return {
            'status': 'error',
            'data': None,
            'details': None
        }
