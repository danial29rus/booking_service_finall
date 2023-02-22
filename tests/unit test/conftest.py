from datetime import datetime
from typing import AsyncGenerator

import pytest
from httpx import AsyncClient
from sqlalchemy import insert, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import NoResultFound

from app.api.endpoints.bookings.models import Bookings
from app.main import app
from tests.conftest import async_session_maker

from app.api.endpoints.auth.router import get_password_hash, verify_password
from app.api.endpoints.auth.models import Users
from app.api.endpoints.hotels.models import Hotels, Rooms



@pytest.fixture(scope="session", name="add_users", autouse=True)
async def add_users_to_database(session: AsyncSession):
    users = [
        {
            "email": "artem@gmail.com",
            "hashed_password": get_password_hash("secret"),
        },
        {
            "email": "roman@mail.ru",
            "hashed_password": get_password_hash("qwerty"),
        },
    ]
    add_users = insert(Users).values(users)
    await session.execute(add_users)
    await session.commit()


@pytest.fixture(scope="session", name="add_hotels_and_rooms")
async def add_hotels_and_rooms_to_database(session: AsyncSession):
    hotels = [
        {
            "name": "Cosmos Collection Altay Resort",
            "location": "Республика Алтай, Майминский район, село Урлу-Аспак, Лесхозная улица, 20",
            "services": [
              "Wi-Fi",
              "Бассейн",
              "Парковка",
              "Кондиционер в номере"
            ],
            "rooms_quantity": 15,
            "image_names": [
              "cosmos_h.webp"
            ],
        },
        {
            "name": "Skala",
            "location": "Республика Алтай, Майминский район, поселок Барангол, Чуйская улица 40а",
            "services": [
                "Wi-Fi",
                "Парковка"
            ],
            "rooms_quantity": 23,
            "image_names": [
                "scala_h.webp"
            ],
        },
        {
            "name": "Palace",
            "location": "Республика Коми, Сыктывкар, Первомайская улица, 62",
            "services": [
                "Wi-Fi",
                "Парковка",
                "Кондиционер в номере"
            ],
            "rooms_quantity": 22,
            "image_names": [
                "sykpalace_h.webp"
            ],
        },
    ]

    rooms = [
        {
            "description": "кайфовое местечко (сменить позже)",
            "hotel_id": 1,
            "price": 22450,
            "image_names": [
                "cosmos_r2.webp"
            ],
            "services": [
                "Бесплатный Wi‑Fi",
                "Кондиционер"
            ],
            "name": "Делюкс Плюс",
            "quantity": 10
        },
        {
            "description": "кайфовое местечко (сменить позже)",
            "hotel_id": 1,
            "price": 24500,
            "image_names": [
                "cosmos_r1.webp"
            ],
            "services": [
                "Бесплатный Wi‑Fi",
                "Кондиционер (с климат-контролем)"
            ],
            "name": "Улучшенный с террасой и видом на озеро",
            "quantity": 5
        },
        {
            "description": "кайфовое местечко (сменить позже)",
            "hotel_id": 2,
            "price": 4570,
            "image_names": [
              "scala_r2.webp"
            ],
            "services": [],
            "name": "Номер на 2-х человек",
            "quantity": 15,
        }
    ]

    add_hotels = insert(Hotels).values(hotels)
    add_rooms = insert(Rooms).values(rooms)
    await session.execute(add_hotels)
    await session.execute(add_rooms)
    await session.commit()

@pytest.mark.usefixtures("add_users_to_database", "add_hotels_and_rooms")
@pytest.fixture(scope="session", name="add_bookings")
async def add_bookings_to_database(session: AsyncSession):
    bookings = [
        {
            "room_id": 2,
            "user_id": 1,
            "date_from": datetime(2023, 2, 10).date(),
            "date_to": datetime(2023, 2, 15).date(),
            "price": 24500,
        },
        {
            "room_id": 2,
            "user_id": 1,
            "date_from": datetime(2023, 2, 13).date(),
            "date_to": datetime(2023, 2, 28).date(),
            "price": 24500,
        },
        {
            "room_id": 3,
            "user_id": 1,
            "date_from": datetime(2023, 2, 13).date(),
            "date_to": datetime(2023, 3, 13).date(),
            "price": 4570,
        },
    ]

    add_bookings = insert(Bookings).values(bookings)
    await session.execute(add_bookings)
    await session.commit()


@pytest.mark.usefixtures("add_users")
@pytest.fixture(scope="function")
async def login_user(
        ac: AsyncClient,
):
    await ac.post("/auth/login", data={
        "email": "artem@gmail.com",
        "password": "secret",
    })