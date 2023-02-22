from datetime import timedelta

from fastapi import Depends, APIRouter
from starlette.responses import Response
from fastapi import status, HTTPException, Request
from fastapi.responses import RedirectResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import insert, select

from app.api.endpoints.auth.manager import authenticate_user, Token, ACCESS_TOKEN_EXPIRE_MINUTES, \
    create_access_token, PasswordRequestForm, PasswordRequestForm, get_password_hash, verify_password
from app.api.endpoints.auth.utils import get_current_user
from app.api.endpoints.auth.models import Users
from app.api.endpoints.auth.schemas import User
from app.database import get_async_session

router = APIRouter(
    tags=["Authentication"],
    prefix="/auth"
)


@router.post("/register", status_code=201)
async def register_user(
        form_data: PasswordRequestForm = Depends(),
        session: AsyncSession = Depends(get_async_session),
):
    hashed_password = get_password_hash(form_data.password)
    check_existing_email = select(Users).filter_by(email=form_data.email)
    existing_user = await session.execute(check_existing_email)
    if existing_user.scalar():  # если пользователь существует, вернуть ошибку
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Пользователь с такой почтой уже существует",
        )
    stmt = insert(Users).values(
        email=form_data.email,
        hashed_password=hashed_password
    )
    await session.execute(stmt)
    await session.commit()

    return None


@router.post("/login", response_model=Token)
async def login_user(
        response: Response,
        form_data: PasswordRequestForm = Depends(),
):
    user = await authenticate_user(form_data.email, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    response.set_cookie("booking_access_token", access_token)
    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/logout")
def logout_user(response: Response):
    response.delete_cookie("booking_access_token")
    return None


@router.get("/users/me")
async def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user
