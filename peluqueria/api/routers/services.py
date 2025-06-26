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
from peluqueria.api.utils.service_utils import (
    check_if_service_exist,
    get_service_or_404,
)
from peluqueria.api.utils.utils import id_to_pydantic, id_to_pydantic_loop

router: APIRouter = APIRouter(prefix="/services", tags=["services"])


@router.post("", response_model=ServiceResponse)
async def create_service(service: Service):
    if await check_if_service_exist(service.name):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Service already registered by another service.",
        )

    service_in_db = ServiceInDB(
        name=service.name,
        description=service.description or None,
        duration_minutes=service.duration_minutes,
        price=service.price,
        created_at=datetime.now(timezone.utc),
        updated_at=datetime.now(timezone.utc),
    )

    service_dict = service_in_db.model_dump()

    service_id = (await db.services.insert_one(service_dict)).inserted_id
    service_dict["id"] = str(service_id)
    return ServiceResponse.model_validate(service_dict)


@router.get("", response_model=list[ServiceResponse])
async def get_all_services():
    services = await db.services.find().to_list(length=None)
    return [
        ServiceResponse.model_validate(id_to_pydantic_loop(service))
        for service in services
    ]


@router.patch("/{service_id}", response_model=ServiceResponse)
async def update_service(
    service_update_data: ServiceUpdateAdmin,
    service_id: str,
    service: Annotated[ServiceResponse, Depends(get_service_or_404)],
):
    update_data = service_update_data.model_dump(exclude_unset=True)

    if not update_data:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No update data provided.",
        )

    if (
        "name" in update_data
        and update_data["name"] != service.name
        and await check_if_service_exist(update_data["name"])
    ):
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

    id_to_pydantic(updated_service_doc)

    return ServiceResponse.model_validate(updated_service_doc)
