from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_async_session
from app.api.endpoints.hotels.models import Hotels, Rooms

router = APIRouter(
    prefix="/hotels",
    tags=["hotels"]
)


@router.get("/location")
async def get_hotel_locations(location_hotel: str, session: AsyncSession = Depends(get_async_session)):
    try:
        query = select(Hotels).where(Hotels.location.contains(location_hotel.title()))
        result = await session.execute(query)
        return result.all()
    except Exception as e:
        print(e)
        return {
            'status': 'error',
            'data': None,
            'details': None
        }


@router.get("/id")
async def get_id_room(session: AsyncSession = Depends(get_async_session)):
    try:
        query = select(Rooms).where(Rooms.quantity_left > 1)
        result = await session.execute(query)
        return result.all()
    except:
        return {
            'status': 'error',
            'data': None,
            'details': None
        }
