from contextlib import asynccontextmanager

from fastapi import FastAPI

from peluqueria.api.db.db_connect import create_indexes
from peluqueria.api.routers import auth, services, users


@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_indexes()
    yield


fastapi_app: FastAPI = FastAPI(lifespan=lifespan)

fastapi_app.include_router(users.router)
fastapi_app.include_router(auth.router)
fastapi_app.include_router(services.router)
