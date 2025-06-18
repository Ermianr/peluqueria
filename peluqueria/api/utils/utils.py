import bcrypt
from fastapi import HTTPException, status

from peluqueria.api.db.db_connect import db
from peluqueria.api.models.user import UserInDBResponse, UserResponse
from peluqueria.api.schemas.user import user_db_response_schema, user_response_schema


def hash_password(password: str) -> str:
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode("utf-8"), salt).decode("utf-8")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(
        plain_password.encode("utf-8"), hashed_password.encode("utf-8")
    )


async def check_if_user_exist(email: str) -> bool:
    user = await db.users.find_one({"email": email})
    return user is not None


async def search_user(field: str, key) -> UserResponse:
    user = await db.users.find_one({field: key})

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found."
        )

    return UserResponse(**user_response_schema(user))


async def search_user_db(field: str, key) -> UserInDBResponse:
    user = await db.users.find_one({field: key})

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )

    return UserInDBResponse(**user_db_response_schema(user))
