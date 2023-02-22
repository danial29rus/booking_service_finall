import asyncio
from typing import AsyncGenerator

from datetime import timedelta, timezone

from fastapi import Depends, Request
from fastapi.responses import RedirectResponse
from jose import JWTError, jwt
from passlib.context import CryptContext
from typing import Union
from fastapi import status, HTTPException, Form
from pydantic import BaseModel
from datetime import datetime
from sqlalchemy.sql import select
from sqlalchemy.exc import NoResultFound

from app.api.endpoints.auth.manager import SECRET_KEY, get_user, ALGORITHM, TokenData, verify_password

import pytest
from pytest import MonkeyPatch
from fastapi.testclient import TestClient
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import NullPool

from app.api.endpoints.auth.utils import oauth2_scheme, get_current_user
from app.api.endpoints.auth.models import Users
from app.database import get_async_session, Base
from app.config import (DB_HOST_TEST, DB_NAME_TEST, DB_PASS_TEST, DB_PORT_TEST,
                        DB_USER_TEST)
from app.main import app as fastapi_app
import app.api.endpoints.auth.router

# DATABASE
DATABASE_URL_TEST = f"postgresql+asyncpg://{DB_USER_TEST}:{DB_PASS_TEST}@{DB_HOST_TEST}:{DB_PORT_TEST}/{DB_NAME_TEST}"

async_engine_test = create_async_engine(DATABASE_URL_TEST, poolclass=NullPool)
async_session_maker = sessionmaker(async_engine_test, class_=AsyncSession, expire_on_commit=False)
Base.metadata.bind = async_engine_test


async def override_get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session


fastapi_app.dependency_overrides[get_async_session] = override_get_async_session


async def patch_get_user(email: str):
    try:
        async with async_session_maker() as session:
            query = select(Users) \
                .filter_by(email=email)
            result = await session.execute(query)
            user_model = result.scalar_one()
            return user_model
    except NoResultFound:
        return None


async def patch_authenticate_user(email: str, password: str):
    user = await patch_get_user(email)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user


@pytest.fixture(autouse=True, scope="function")
def patch_authenticate(monkeypatch: MonkeyPatch):
    monkeypatch.setattr(app.api.endpoints.auth.router, "authenticate_user", patch_authenticate_user)


async def override_get_current_user(
        token: str = Depends(oauth2_scheme),
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
    )
    expire_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Credentials expired",
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        expire: str = payload.get("exp")
        if int(expire) - datetime.now(timezone.utc).timestamp() < 0:
            raise expire_exception
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
        token_data = TokenData(email=email)
    except JWTError:
        raise credentials_exception
    user = await patch_get_user(token_data.email)
    if user is None:
        raise credentials_exception
    return user


fastapi_app.dependency_overrides[get_current_user] = override_get_current_user


@pytest.fixture(scope='session', autouse=True)
async def prepare_database():
    async with async_engine_test.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with async_engine_test.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest.fixture(scope='session')
def event_loop(request):
    """Create an instance of the default event loop for each test case."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="session")
async def session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session


client = TestClient(fastapi_app)


@pytest.fixture(scope="session")
async def ac() -> AsyncGenerator[AsyncClient, None]:
    async with AsyncClient(app=fastapi_app, base_url="http://test") as ac:
        yield ac
