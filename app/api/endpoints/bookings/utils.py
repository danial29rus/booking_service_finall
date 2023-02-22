from app.api.endpoints.bookings.models import Bookings
from app.api.endpoints.hotels.models import Hotels, Rooms
from sqlalchemy import select


async def get_booking_info(booking_id: int, session):
    get_booking = select(
        Hotels.name.label("hotel_name"),
        Rooms.name.label("room_name"),
        Rooms.description.label("room_description"),
        Bookings.date_from,
        Bookings.date_to,
        Bookings.total_cost,
        Bookings.total_days,
    ).select_from(Bookings).filter_by(
        id=booking_id
    ).join(
        Rooms, Rooms.id == Bookings.room_id
    ).join(
        Hotels, Hotels.id == Rooms.hotel_id
    )

    booking_info = await session.execute(get_booking)
    booking_info = booking_info.one_or_none()
    return booking_info