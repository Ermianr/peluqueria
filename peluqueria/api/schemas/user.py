def user_response_schema(user) -> dict:
    return {
        "first_name": user.get("first_name", ""),
        "last_name": user.get("last_name", ""),
        "email": user.get("email", ""),
        "phone": user.get("phone", ""),
        "id": str(user.get("_id", "")),
        "created_at": user.get("created_at", ""),
        "updated_at": user.get("updated_at", ""),
        "is_active": user.get("is_active", ""),
    }


def user_db_response_schema(user) -> dict:
    return {
        "first_name": user.get("first_name", ""),
        "last_name": user.get("last_name", ""),
        "email": user.get("email", ""),
        "phone": user.get("phone", ""),
        "id": str(user.get("_id", "")),
        "hashed_password": user.get("hashed_password", ""),
        "created_at": user.get("created_at", ""),
        "updated_at": user.get("updated_at", ""),
        "is_active": user.get("is_active", ""),
    }
