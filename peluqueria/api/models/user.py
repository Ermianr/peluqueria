from datetime import datetime
from typing import Annotated

from pydantic import BaseModel, EmailStr, StringConstraints

from peluqueria.constants import PHONE_REGEX

Name = Annotated[str, StringConstraints(strip_whitespace=True, min_length=4)]
Phone = Annotated[str, StringConstraints(pattern=PHONE_REGEX)]


class User(BaseModel):
    first_name: Name
    last_name: Name
    email: EmailStr
    phone: Phone


class UserCreate(User):
    password: str


class UserInDB(User):
    id: str | None = None
    hashed_password: str
    created_at: datetime | None = None
    updated_at: datetime | None = None
    is_active: bool = True


class UserResponse(User):
    id: str
    created_at: datetime
    updated_at: datetime
    is_active: bool
