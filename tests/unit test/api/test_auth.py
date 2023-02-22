import pytest
from sqlalchemy import insert

from tests.conftest import client, async_session_maker
from app.api.endpoints.auth.models import Users
from httpx import AsyncClient
from app.main import app
from app.api.endpoints.auth.models import Users


async def test_append_users():
    async with async_session_maker() as session:
        userss = insert(Users).values(email="string10",
                                     hashed_password="string10"
                                     )

        await session.execute(userss)
        await session.commit()


def test_register():
    response = client.post("/auth/register", json={
        "email": "string",
        "password": "string"
    })

    assert response.status_code == 201


async def test_create_user(authenticate: AsyncClient):
    response = await authenticate.post("/auth/register", json={"username": "string1", "email": "testuser@nofoobar.com",
                                                               "password": "string1"})
    assert response.status_code == 201
    assert response.json()["email"] == "testuser@nofoobar.com"
    assert response.json()["is_active"] == True



@pytest.mark.usefixtures("test_app")
async def test_login_in(authenticate: AsyncClient):

    response_log = await authenticate.post("/auth/login", json={
        "username": "string",
        "password": "string"
    })
    response_bok = await authenticate.post("/booking_hotel", json={
        "room_id": 5,
        "date_from": "2023-02-12T15:22:01.163Z",
        "date_to": "2023-02-12T15:22:01.163Z"
    })

    assert response_log.status_code == 200
    assert response_bok.status_code == 201
