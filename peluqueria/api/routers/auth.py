from datetime import datetime, timedelta, timezone
from typing import Annotated

import jwt
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jwt import InvalidTokenError

from peluqueria.api.models.auth import Token
from peluqueria.api.models.user import UserInDBResponse, UserResponse
from peluqueria.api.utils.user_utils import search_user_db
from peluqueria.api.utils.utils import verify_password
from peluqueria.settings import Settings

ALGORITHM = "HS256"
SECRET_KEY = Settings.HASH_PASSWORD_SECRET_KEY
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24 * Settings.ACCESS_TOKEN_EXPIRE_DAYS

router: APIRouter = APIRouter(prefix="/auth", tags=["authentication"])

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


async def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)],
) -> UserInDBResponse:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email = payload.get("sub")

        if email is None:
            raise credentials_exception

        user = await search_user_db("email", email)
    except InvalidTokenError as exc:
        raise credentials_exception from exc
    except HTTPException as exc:
        raise credentials_exception from exc

    return user


async def get_current_active_user(
    current_user: Annotated[UserInDBResponse, Depends(get_current_user)],
) -> UserInDBResponse:
    if not current_user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


@router.post("/login", response_model=Token)
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    try:
        user: UserInDBResponse = await search_user_db(
            "email",
            form_data.username,
        )
    except HTTPException as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Correo incorrecto.",
            headers={"WWW-Authenticate": "Bearer"},
        ) from exc

    if not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Contraseña incorrecta.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token({"sub": user.email}, access_token_expires)

    return Token(access_token=access_token, token_type="bearer")


@router.get("/me", response_model=UserResponse)
async def me(
    current_user: Annotated[UserInDBResponse, Depends(get_current_active_user)],
):
    return UserResponse(
        id=str(current_user.id),
        role=current_user.role,
        first_name=current_user.first_name,
        last_name=current_user.last_name,
        email=current_user.email,
        phone=current_user.phone,
        is_active=current_user.is_active,
        created_at=current_user.created_at,
        updated_at=current_user.updated_at,
    )
