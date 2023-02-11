import json
from typing import Optional

from fastapi_users import schemas
from pydantic import BaseModel, json


class Hotel(BaseModel):
    id: int
    name: str
    category_id: int
    location: str
    services: list



