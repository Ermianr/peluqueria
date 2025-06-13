from fastapi import FastAPI

from peluqueria.api.routers import auth, users

fastapi_app: FastAPI = FastAPI()

fastapi_app.include_router(users.router)
fastapi_app.include_router(auth.router)
