# from datetime import datetime, timedelta
# from fastapi import APIRouter, Depends, HTTPException, Query, status
# from pydantic import BaseModel, Field
# from typing import Optional
# from sqlalchemy import select, insert
#
# from sqlalchemy.ext.asyncio import AsyncSession
#
# from app.api.endpoints.auth.models import Users
# from passlib.context import CryptContext
# from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
# import json
# from jose import jwt, JWTError
# from app.api.endpoints.auth.schemas import NewUser, Token, TokenData
# from app.config import SECRET_AUTH
# from app.database import get_async_session
#
# router = APIRouter(
#     prefix="/users",
#     tags=["users"],
#     responses={404: {"description": "Not found"}}
# )
#
# crypt_context = CryptContext(schemes=["sha256_crypt", "md5_crypt"])
#
#
# def create_access_token(data: dict, expires_delta: timedelta):
#     to_encode = data.copy()
#     expire = datetime.utcnow() + expires_delta
#     to_encode.update({"exp": expire})
#     encoded_jwt = jwt.encode(to_encode, SECRET_AUTH, algorithm='HS256')
#     return encoded_jwt
#
#
# def verify_password(plain_password, hashed_password):
#     return crypt_context.verify(plain_password, hashed_password)
#
#
# def authenticate(username, password):
#     user = get_user(username)
#     password_check = verify_password(password, user['password'])
#     return password_check
#
#
# def get_password_hash(password):
#     return crypt_context.hash(password)
#
#
# oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
#
#
# @router.post("/signup")
# async def sign_up(newUser: NewUser, session: AsyncSession = Depends(get_async_session)):
#     stmt = insert(Users).values(email=newUser.username,
#                                 hashed_password=get_password_hash(newUser.hashed_password))
#     await session.execute(stmt)
#     await session.commit()
#     return {"message": "Created user successfully!"}
#
#
# @router.post("/token", response_model=Token)
# async def login(form_data: OAuth2PasswordRequestForm = Depends()):
#     username = form_data.username
#     password = form_data.password
#     if authenticate(username, password):
#         access_token = create_access_token(
#             data={"sub": username}, expires_delta=timedelta(minutes=30))
#         return {"access_token": access_token, "token_type": "bearer"}
#     else:
#         raise HTTPException(
#             status_code=400, detail="Incorrect username or password")
#
#
# def get_user(username: str, session: AsyncSession = Depends(get_async_session)):
#     try:
#         query = select(Users).where(Users.c.email == username)
#         result = await session.execute(query)
#         return result.all()
#     except:
#         return {
#             'status': 'error',
#             'data': None,
#             'details': None
#         }
#
#
# async def get_current_user(token: str = Depends(oauth2_scheme)):
#     credentials_exception = HTTPException(
#         status_code=status.HTTP_401_UNAUTHORIZED,
#         detail="Could not validate credentials",
#         headers={"WWW-Authenticate": "Bearer"},
#     )
#     try:
#         payload = jwt.decode(token, SECRET_AUTH, algorithms=["SH256"])
#         username: str = payload.get("sub")
#         if username is None:
#             raise credentials_exception
#         token_data = TokenData(username=username)
#     except JWTError:
#         raise credentials_exception
#     user = get_user(username=token_data.username)
#     if user is None:
#         raise credentials_exception
#     return user
#
#
# @router.get("/detail")
# async def user_detail(current_user: Users = Depends(get_current_user)):
#     return {"name": "Danny", "email": "danny@tutorialsbuddy.com"}
