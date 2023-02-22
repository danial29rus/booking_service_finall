
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

from app.api.endpoints.auth.manager import SECRET_KEY, get_user, ALGORITHM, TokenData
from app.api.endpoints.auth.models import Users
from app.database import async_session_maker


class CustomOAuth2:
    async def __call__(self, request: Request) -> str:
        token = request.cookies.get("booking_access_token")
        if not token:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Not authenticated"
            )

        return token

# то же самое, только в виде функции
def custom_oauth2(request: Request):
    token = request.cookies.get("booking_access_token")
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated"
        )

    return token


oauth2_scheme = custom_oauth2


async def get_current_user(
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
    user = await get_user(token_data.email)
    if user is None:
        raise credentials_exception
    return user
