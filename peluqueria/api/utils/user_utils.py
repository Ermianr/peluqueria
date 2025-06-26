from typing import Any

from bson import ObjectId
from fastapi import HTTPException, status

from peluqueria.api.db.db_connect import db
from peluqueria.api.models.user import UserInDBResponse, UserResponse
from peluqueria.api.utils.utils import id_to_pydantic


async def check_if_user_exist(email: str) -> bool:
    user = await db.users.find_one({"email": email})
    return user is not None


async def search_user(field: str, key: Any) -> UserResponse:
    user = await db.users.find_one({field: key})

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found.",
        )
    id_to_pydantic(user)

    return UserResponse.model_validate(user)


async def search_user_db(field: str, key: Any) -> UserInDBResponse:
    user = await db.users.find_one({field: key})

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )

    id_to_pydantic(user)

    return UserInDBResponse.model_validate(user)


### Dependencia para buscar usuarios
async def get_user_or_404(user_id: str) -> UserResponse | HTTPException:
    return await search_user("_id", ObjectId(user_id))
