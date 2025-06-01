from fastapi import FastAPI
from peluqueria.api.routers import users

fastapi_app: FastAPI = FastAPI()

fastapi_app.include_router(users.router)



