from datetime import datetime

from pydantic import BaseModel

from peluqueria.api.models.types import DateCo


class Appointment(BaseModel):
    user_id: str
    employee_id: str
    service_ids: list[str]
    appointment_date: datetime


class AppointmentInDB(Appointment):
    employee_name: str
    service_names: list[str]
    user_name: str
    created_at: datetime
    updated_at: datetime
    state: str
    total_cost: float


class AppointmentResponse(Appointment):
    id: str
    employee_name: str
    user_name: str
    service_names: list[str]
    appointment_date: DateCo
    created_at: DateCo
    updated_at: DateCo
    state: str
    total_cost: float
