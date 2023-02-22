from pydantic import BaseModel, EmailStr


class User(BaseModel):
    id: int
    email: EmailStr

    class Config:
        orm_mode = True


class UserInDB(User):
    hashed_password: str
