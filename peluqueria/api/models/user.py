from datetime import datetime
from typing import Annotated

from pydantic import BaseModel, EmailStr, StringConstraints

Name = Annotated[str, StringConstraints(strip_whitespace=True, min_length=4)]
Phone = Annotated[str, StringConstraints(pattern=r"^3\d{9}$")]


class User(BaseModel):
    first_name: Name
    last_name: Name
    email: EmailStr
    phone: Phone
    password: str
    created_at: datetime | None = None
    updated_at: datetime | None = None


class UserCreationResponse(BaseModel):
    id: str


class UserFindResponse(BaseModel):
    id: str
    first_name: str
    last_name: str
    email: str
    phone: str
