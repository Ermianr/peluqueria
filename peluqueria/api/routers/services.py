from datetime import datetime, timezone
from typing import Annotated

from bson import ObjectId
from fastapi import APIRouter, Depends, HTTPException, status

from peluqueria.api.db.db_connect import db
from peluqueria.api.models.service import (
    Service,
    ServiceInDB,
    ServiceResponse,
    ServiceUpdateAdmin,
)

router: APIRouter = APIRouter(prefix="/services", tags=["services"])


@router.post("", response_model=ServiceResponse)
async def create_service(service: Service):
    service_in_db = ServiceInDB(
        name=service.name,
        description=service.description or None,
        duration_minutes=service.duration_minutes,
        price=service.price,
        created_at=datetime.now(timezone.utc),
        updated_at=datetime.now(timezone.utc),
    )

    service_dict = service_in_db.model_dump()

    id = (await db.services.insert_one(service_dict)).inserted_id
    service_dict["id"] = str(id)
    return ServiceResponse.model_validate(service_dict)


### Helper para transformar los id a formato pydantic
def transform_id(doc: dict) -> dict:
    if "_id" in doc:
        doc["id"] = str(doc["_id"])
        del doc["_id"]
    return doc


@router.get("", response_model=list[ServiceResponse])
async def get_all_services():
    services = await db.services.find().to_list(length=None)
    return [
        ServiceResponse.model_validate(transform_id(service)) for service in services
    ]


### Helper para buscar
async def check_if_service_exist(name: str) -> bool:
    service = await db.services.find_one({"name": name})
    return service is not None


async def get_service_or_404(id: str) -> ServiceResponse:
    service = await db.services.find_one({"_id": ObjectId(id)})
    if not service:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Service not found."
        )
    service["id"] = str(service["_id"])
    del service["_id"]
    return ServiceResponse.model_validate(service)


@router.patch("/{id}", response_model=ServiceResponse)
async def update_user(
    service_update_data: ServiceUpdateAdmin,
    service: Annotated[ServiceResponse, Depends(get_service_or_404)],
):
    update_data = service_update_data.model_dump(exclude_unset=True)

    if not update_data:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No update data provided.",
        )

    if "name" in update_data and update_data["name"] != service.name:
        if await check_if_service_exist(update_data["name"]):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Service already registered by another service.",
            )

    update_data["updated_at"] = datetime.now(timezone.utc)

    updated_service_doc = await db.services.find_one_and_update(
        {"_id": ObjectId(service.id)},
        {"$set": update_data},
        return_document=True,
    )

    if not updated_service_doc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Service not found after update.",
        )

    updated_service_doc["id"] = str(updated_service_doc["_id"])
    del updated_service_doc["_id"]

    return ServiceResponse.model_validate(updated_service_doc)
