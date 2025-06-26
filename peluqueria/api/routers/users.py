from datetime import datetime, timezone
from typing import Annotated

from bson import ObjectId
from fastapi import APIRouter, Depends, HTTPException, status

from peluqueria.api.db.db_connect import db
from peluqueria.api.models.user import (
    UserCreate,
    UserInDB,
    UserResponse,
    UserUpdateAdmin,
)
from peluqueria.api.utils.user_utils import (
    check_if_user_exist,
    get_user_or_404,
    search_user,
)
from peluqueria.api.utils.utils import (
    hash_password,
    id_to_pydantic,
    id_to_pydantic_loop,
)

router: APIRouter = APIRouter(prefix="/users", tags=["users"])

### Crear usuarios


@router.post("", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def create_user(user: UserCreate):
    if await check_if_user_exist(user.email):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="User already exist."
        )
    # Transformar la request al objeto UserInDB
    user_in_db = UserInDB(
        first_name=user.first_name,
        last_name=user.last_name,
        email=user.email,
        phone=user.phone,
        role="customer",
        hashed_password=hash_password(user.password),
        created_at=datetime.now(timezone.utc),
        updated_at=datetime.now(timezone.utc),
        is_active=True,
    )
    # Transformar UserInDB a dict para poder guardar en mongoDB
    user_dict = user_in_db.model_dump()

    user_id = (await db.users.insert_one(user_dict)).inserted_id
    user_dict["id"] = str(user_id)
    return UserResponse.model_validate(user_dict)


### Buscar todos los usuarios


@router.get("", response_model=list[UserResponse])
async def get_users():
    users = await db.users.find({"role": "customer"}).to_list(length=None)
    return [UserResponse.model_validate(id_to_pydantic_loop(user)) for user in users]


### Buscar usuarios por su ID endpoint


@router.get("/{user_id}", response_model=UserResponse)
async def get_user(
    user_id: str, user: Annotated[UserResponse, Depends(get_user_or_404)]
):
    return user


### Actualizar un usuario por su ID
@router.patch("/{user_id}", response_model=UserResponse)
async def update_user(
    user_update_data: UserUpdateAdmin,
    user_id: str,
    user: Annotated[UserResponse, Depends(get_user_or_404)],
):
    update_data = user_update_data.model_dump(exclude_unset=True)

    if not update_data:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No update data provided.",
        )

    if (
        "email" in update_data
        and update_data["email"] != user.email
        and await check_if_user_exist(update_data["email"])
    ):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email already registered by another user.",
        )

    update_data["updated_at"] = datetime.now(timezone.utc)

    updated_user_doc = await db.users.find_one_and_update(
        {"_id": ObjectId(user.id)},
        {"$set": update_data},
        return_document=True,
    )

    if not updated_user_doc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found after update."
        )

    id_to_pydantic(updated_user_doc)

    return UserResponse.model_validate(updated_user_doc)


@router.delete("/{user_id}")
async def delete_user(user_id: str):
    try:
        await search_user("_id", ObjectId(user_id))
    except HTTPException as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found."
        ) from exc
    await db.users.delete_one({"_id": ObjectId(user_id)})

    return {"detail": "User deleted."}
