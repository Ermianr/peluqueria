from typing import Any

from bson import ObjectId
from fastapi import HTTPException, status

from peluqueria.api.db.db_connect import db
from peluqueria.api.models.service import ServiceResponse
from peluqueria.api.utils.utils import id_to_pydantic


async def serach_service(field: str, key: Any) -> ServiceResponse:
    service = await db.services.find_one({field: ObjectId(key)})

    if not service:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Service not found."
        )

    id_to_pydantic(service)

    return ServiceResponse.model_validate(service)


async def get_service_or_404(service_id: str) -> ServiceResponse:
    return await serach_service("_id", ObjectId(service_id))


async def check_if_service_exist(name: str) -> bool:
    service = await db.services.find_one({"name": name})
    return service is not None
