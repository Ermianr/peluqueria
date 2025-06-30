from typing import Any

from bson import ObjectId
from fastapi import HTTPException, status

from peluqueria.api.db.db_connect import db
from peluqueria.api.models.user import UserInDBResponse, UserResponse
from peluqueria.api.utils.utils import id_to_pydantic


async def check_if_user_exist(email: str) -> bool:
    data_user = await db.users.find_one({"email": email})
    data_employee = await db.employees.find_one({"email": email})
    return data_user is not None or data_employee is not None


async def search_user(field: str, key: Any, user_type: str) -> UserResponse:
    data = {}
    if user_type == "user":
        data = await db.employees.find_one({field: key})
    else:
        data = await db.users.find_one({field: key})

    if not data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found.",
        )
    id_to_pydantic(data)

    return UserResponse.model_validate(data)


async def search_user_db(field: str, key: Any) -> UserInDBResponse:
    data = await db.users.find_one({field: key})

    if not data:
        data = await db.employees.find_one({field: key})

    if not data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )

    id_to_pydantic(data)

    return UserInDBResponse.model_validate(data)


### Dependencia para buscar usuarios
async def get_user_or_404(user_id: str, user_type: str) -> UserResponse | HTTPException:
    return await search_user("_id", ObjectId(user_id), user_type)


async def get_employee_or_404(user_id: str) -> UserResponse | HTTPException:
    return await search_user("_id", ObjectId(user_id), "employee")


async def get_customer_or_404(user_id: str) -> UserResponse | HTTPException:
    return await search_user("_id", ObjectId(user_id), "customer")
