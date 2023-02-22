from datetime import datetime

from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTable
from sqlalchemy import Column, Integer, String, TIMESTAMP, Boolean

from app.database import Base


class Users(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, nullable=False)
    email = Column(String, nullable=False)
    hashed_password = Column(String, nullable=False)
