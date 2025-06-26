import bcrypt


def hash_password(password: str) -> str:
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode("utf-8"), salt).decode("utf-8")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(
        plain_password.encode("utf-8"), hashed_password.encode("utf-8")
    )


def id_to_pydantic(doc: dict) -> None:
    doc["id"] = str(doc["_id"])
    del doc["_id"]


### Helper para un bucle y transformar un id a formato pydantic
def id_to_pydantic_loop(doc: dict) -> dict:
    if "_id" in doc:
        id_to_pydantic(doc)
    return doc
