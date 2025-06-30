import logging
from datetime import datetime, timezone

from bson import ObjectId
from fastapi import APIRouter, HTTPException, status

from peluqueria.api.db.db_connect import db
from peluqueria.api.models.appointments import (
    Appointment,
    AppointmentInDB,
    AppointmentResponse,
)

logger = logging.getLogger(__name__)

router: APIRouter = APIRouter(prefix="/appointments", tags=["appointments"])


@router.post(
    "",
    response_model=AppointmentResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_appointment(appointment: Appointment):
    user_name = await db.users.find_one(
        {"_id": ObjectId(appointment.user_id)},
        {"first_name": 1, "last_name": 1, "_id": 0},
    )
    employee_name = await db.employees.find_one(
        {"_id": ObjectId(appointment.employee_id)},
        {"first_name": 1, "last_name": 1, "_id": 0},
    )

    service_names = []
    total_cost = 0.0

    for service_id in appointment.service_ids:
        service = await db.services.find_one(
            {"_id": ObjectId(service_id)},
            {"name": 1, "price": 1, "_id": 0},
        )
        if service:
            service_names.append(service.get("name", ""))
            total_cost += service.get("price", 0)

    employee_full_name = ""
    if employee_name:
        first_name = employee_name.get("first_name", "")
        last_name = employee_name.get("last_name", "")
        employee_full_name = f"{first_name} {last_name}"

    user_full_name = ""
    if user_name:
        first_name = user_name.get("first_name", "")
        last_name = user_name.get("last_name", "")
        user_full_name = f"{first_name} {last_name}"

    appointment_in_db = AppointmentInDB(
        user_id=appointment.user_id,
        employee_id=appointment.employee_id,
        service_ids=appointment.service_ids,
        appointment_date=appointment.appointment_date,
        created_at=datetime.now(timezone.utc),
        updated_at=datetime.now(timezone.utc),
        employee_name=employee_full_name,
        user_name=user_full_name,
        service_names=service_names,
        state="pending",
        total_cost=total_cost,
    )

    appointment_dict = appointment_in_db.model_dump()
    appointment_id = (await db.appointments.insert_one(appointment_dict)).inserted_id
    appointment_dict["id"] = str(appointment_id)

    return AppointmentResponse.model_validate(appointment_dict)


@router.get("", response_model=list[AppointmentResponse])
async def get_appointments():
    appointments = await db.appointments.find().to_list(length=None)

    for appointment in appointments:
        appointment["id"] = str(appointment.pop("_id"))

        if not appointment.get("user_name") and appointment.get("user_id"):
            user_name = await db.users.find_one(
                {"_id": ObjectId(appointment["user_id"])},
                {"first_name": 1, "last_name": 1, "_id": 0},
            )
            if user_name:
                first_name = user_name.get("first_name", "")
                last_name = user_name.get("last_name", "")
                appointment["user_name"] = f"{first_name} {last_name}"
            else:
                appointment["user_name"] = "Usuario no encontrado"

        if not appointment.get("employee_name") and appointment.get("employee_id"):
            employee_name = await db.employees.find_one(
                {"_id": ObjectId(appointment["employee_id"])},
                {"first_name": 1, "last_name": 1, "_id": 0},
            )
            if employee_name:
                first_name = employee_name.get("first_name", "")
                last_name = employee_name.get("last_name", "")
                appointment["employee_name"] = f"{first_name} {last_name}"
            else:
                appointment["employee_name"] = "Empleado no encontrado"

        if not appointment.get("service_names") and appointment.get("service_ids"):
            service_names = []
            for service_id in appointment["service_ids"]:
                service = await db.services.find_one(
                    {"_id": ObjectId(service_id)},
                    {"name": 1, "_id": 0},
                )
                if service:
                    service_names.append(service.get("name", ""))
            appointment["service_names"] = service_names

    return [
        AppointmentResponse.model_validate(appointment) for appointment in appointments
    ]


@router.get("/{appointment_id}", response_model=AppointmentResponse)
async def get_appointment(appointment_id: str):
    appointment = await db.appointments.find_one({"_id": ObjectId(appointment_id)})
    if not appointment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Appointment not found.",
        )
    appointment["id"] = str(appointment.pop("_id"))
    return AppointmentResponse.model_validate(appointment)


@router.delete("/{appointment_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_appointment(appointment_id: str):
    result = await db.appointments.delete_one({"_id": ObjectId(appointment_id)})
    if result.deleted_count == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Appointment not found.",
        )


@router.patch("/{appointment_id}", response_model=AppointmentResponse)
async def update_appointment(appointment_id: str, update_data: dict):
    update_data["updated_at"] = datetime.now(timezone.utc)

    result = await db.appointments.update_one(
        {"_id": ObjectId(appointment_id)},
        {"$set": update_data},
    )

    if result.modified_count == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Appointment not found.",
        )

    updated_appointment = await db.appointments.find_one(
        {"_id": ObjectId(appointment_id)},
    )
    if not updated_appointment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Appointment not found after update.",
        )

    updated_appointment["id"] = str(updated_appointment.pop("_id"))
    return AppointmentResponse.model_validate(updated_appointment)
