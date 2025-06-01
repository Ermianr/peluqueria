from datetime import datetime

from bson import ObjectId
from fastapi import APIRouter, HTTPException, status

from peluqueria.api.db.db_connect import db
from peluqueria.api.models.user import User, UserCreationResponse, UserFindResponse
from peluqueria.api.schemas.user import creation_user_schema
from peluqueria.api.utils.utils import hash_password, search_user

router: APIRouter = APIRouter(prefix="/users", tags=["users"])

### Crear usuarios


@router.post(
    "/", response_model=UserCreationResponse, status_code=status.HTTP_201_CREATED
)
async def create_user(user: User) -> UserCreationResponse:
    if type(await search_user("email", user.email)) is UserFindResponse:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="User already exist."
        )
    # Transformar la request a un dict de python
    user_dict = dict(user)

    # Generar la fecha de creación del usuario
    user_dict["created_at"] = datetime.now()

    # Hashear la contraseña y remplazarla
    hashed_password = hash_password(user_dict["password"])
    user_dict["password"] = hashed_password

    id = (await db.users.insert_one(user_dict)).inserted_id
    inserted_user = creation_user_schema(await db.users.find_one({"_id": id}))
    return UserCreationResponse(**inserted_user)


### Buscar usuarios por su ID


@router.get("/{id}", response_model=UserFindResponse)
async def get_user(id: str) -> UserFindResponse | dict[str, str]:
    return await search_user("_id", ObjectId(id))
