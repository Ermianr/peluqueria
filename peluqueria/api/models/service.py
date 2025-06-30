from datetime import datetime

from pydantic import BaseModel

from peluqueria.api.models.types import DateCo


class Service(BaseModel):
    name: str
    description: str | None = None
    duration_minutes: int
    price: int
    img_path: str


class ServiceInDB(Service):
    created_at: datetime
    updated_at: datetime


class ServiceResponse(Service):
    id: str
    created_at: DateCo
    updated_at: DateCo


class ServiceUpdateAdmin(BaseModel):
    name: str | None = None
    description: str | None = None
    duration_minutes: int | None = None
    price: int | None = None
