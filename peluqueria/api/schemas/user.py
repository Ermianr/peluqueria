def user_response_schema(user) -> dict:
    return {
        "first_name": user["first_name"],
        "last_name": user["last_name"],
        "email": user["email"],
        "phone": user["phone"],
        "id": str(user["_id"]),
        "role": user["role"],
        "created_at": user["created_at"],
        "updated_at": user["updated_at"],
        "is_active": user["is_active"],
    }


def users_response_schema(users) -> list:
    return [user_response_schema(user) for user in users]


def user_db_response_schema(user) -> dict:
    return {
        "first_name": user["first_name"],
        "last_name": user["last_name"],
        "email": user["email"],
        "phone": user["phone"],
        "id": str(user.get("_id", "")),
        "role": user["role"],
        "hashed_password": user["hashed_password"],
        "created_at": user["created_at"],
        "updated_at": user["updated_at"],
        "is_active": user["is_active"],
    }
