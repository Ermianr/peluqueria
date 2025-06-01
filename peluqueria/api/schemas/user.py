def creation_user_schema(user) -> dict:
    return {
        "id": str(user.get("_id", "")),
    }


def find_user_schema(user) -> dict:
    return {
        "id": str(user.get("_id", "")),
        "first_name": user.get("first_name", ""),
        "last_name": user.get("last_name", ""),
        "email": user.get("email", ""),
        "phone": user.get("phone", ""),
    }
