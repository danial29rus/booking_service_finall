import json

from httpx import AsyncClient
from sqlalchemy import insert, select

from app.api.endpoints.auth.models import Users
from app.api.endpoints.hotels.models import Rooms, Hotels, HotelsCategories
from conftest import client, async_session_maker


async def test_add_room():
    async with async_session_maker() as session:
        stmt_category = insert(HotelsCategories).values(name="Гостиница")
        stmt_hotels = insert(Hotels).values(name='Cosmos Collection Altay Resort', category_id=1,
                                            location='Республика Алтай, Майминский район, село Урлу-Аспак, Лесхозная улица, 20',
                                            services='["Wi-Fi", "Бассейн", "Парковка", "Кондиционер в номере"]')
        stmt_Rooms = insert(Rooms).values(hotel_id=1, name='Улучшенный с террасой и видом на озеро', price=24500,
                                          quantity=5, quantity_left=5,
                                          services='["Бесплатный Wi‑Fi", "Кондиционер (с климат-контролем)"]')

        await session.execute(stmt_category)
        await session.execute(stmt_hotels)
        await session.execute(stmt_Rooms)
        await session.commit()


async def test_room(authenticate: AsyncClient):
    response = await authenticate.get("/hotels/id")
    assert response.status_code == 200


async def test_get_specific_operations(authenticate: AsyncClient):
    response = await authenticate.get("/hotels/location", params={
        "location_hotel": "алтай",
    })

    assert response.status_code == 200


