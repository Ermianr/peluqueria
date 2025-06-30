from contextlib import asynccontextmanager

from fastapi import FastAPI

from peluqueria.api.db.db_connect import create_indexes
from peluqueria.api.routers import (
    appointments,
    auth,
    employees,
    reports,
    services,
    users,
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_indexes()
    yield


fastapi_app: FastAPI = FastAPI()

fastapi_app.include_router(users.router)
fastapi_app.include_router(auth.router)
fastapi_app.include_router(services.router)
fastapi_app.include_router(employees.router)
fastapi_app.include_router(appointments.router)
fastapi_app.include_router(reports.router)
