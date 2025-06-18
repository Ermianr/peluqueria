from datetime import datetime

from pydantic import BaseModel, EmailStr

from peluqueria.api.models.types import DateCo, Name, Phone


class User(BaseModel):
    first_name: Name
    last_name: Name
    email: EmailStr
    phone: Phone


class UserCreate(User):
    password: str


class UserInDB(User):
    role: str
    hashed_password: str
    created_at: datetime
    updated_at: datetime
    is_active: bool = True


class UserInDBResponse(UserInDB):
    id: str


class UserResponse(User):
    id: str
    role: str
    created_at: DateCo
    updated_at: DateCo
    is_active: bool


class UserUpdateAdmin(BaseModel):
    first_name: Name | None = None
    last_name: Name | None = None
    email: EmailStr | None = None
    phone: Phone | None = None
    is_active: bool | None = None
