import os

from dotenv import load_dotenv

load_dotenv()


class Settings:
    MONGO_DB_URI: str = os.getenv("MONGO_DB_URI") or "mongodb://localhost:27017/"
    MONGO_DB_NAME: str = os.getenv("MONGO_DB_NAME") or "local"
    API_BACKEND_URL: str = os.getenv("API_BACKEND_URL") or "http://localhost:8000"
    HASH_PASSWORD_SECRET_KEY: str = os.getenv("HASH_PASSWORD_SECRET_KEY=") or "default"
    ACCESS_TOKEN_EXPIRE_DAYS: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_DAYS") or 3)
