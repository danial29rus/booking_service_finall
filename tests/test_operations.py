import json

from httpx import AsyncClient
from sqlalchemy import insert, select

from app.api.endpoints.auth.models import Users
from app.api.endpoints.hotels.models import Rooms, Hotels, HotelsCategories
from conftest import client, async_session_maker



async def dashboard(ac: AsyncClient):
    response = await ac.get("/report/dashboard")

    assert response.status_code == 200
