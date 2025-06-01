import bcrypt

from peluqueria.api.db.db_connect import db
from peluqueria.api.models.user import UserFindResponse
from peluqueria.api.schemas.user import find_user_schema


def hash_password(password: str) -> str:
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode("utf-8"), salt).decode("utf-8")


async def search_user(field: str, key) -> UserFindResponse | dict[str, str]:
    try:
        user = await db.users.find_one({field: key})
        return UserFindResponse(**find_user_schema(user))
    except:
        return {"error": "User not found"}
