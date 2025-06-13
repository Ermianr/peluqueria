from datetime import datetime, timezone

from bson import ObjectId
from fastapi import APIRouter, HTTPException, status

from peluqueria.api.db.db_connect import db
from peluqueria.api.models.user import UserCreate, UserInDB, UserResponse
from peluqueria.api.schemas.user import user_response_schema
from peluqueria.api.utils.utils import check_if_user_exist, hash_password, search_user

router: APIRouter = APIRouter(prefix="/users", tags=["users"])

### Crear usuarios


@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def create_user(user: UserCreate) -> UserResponse:
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
        hashed_password=hash_password(user.password),
        created_at=datetime.now(timezone.utc),
        updated_at=datetime.now(timezone.utc),
        is_active=True,
    )
    # Transformar UserInDB a dict para poder guardar en mongoDB
    user_dict: dict = dict(user_in_db)

    id = (await db.users.insert_one(user_dict)).inserted_id
    inserted_user = user_response_schema(await db.users.find_one({"_id": id}))
    return UserResponse(**inserted_user)


### Buscar usuarios por su ID


@router.get("/{id}", response_model=UserResponse)
async def get_user(id: str) -> UserResponse | dict[str, str]:
    return await search_user("_id", ObjectId(id))
