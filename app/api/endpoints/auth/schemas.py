from typing import Optional

from fastapi_users import schemas
from pydantic import BaseModel


class NewUser(BaseModel):
    username: str
    hashed_password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Optional[str] = None