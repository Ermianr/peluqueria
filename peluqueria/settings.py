import os

from dotenv import load_dotenv

load_dotenv()


class Settings:
    MONGO_DB_URI: str = os.getenv("MONGO_DB_URI") or "mongodb://localhost:27017/"
    MONGO_DB_NAME: str = os.getenv("MONGO_DB_NAME") or "local"
    API_BACKEND_URL: str = os.getenv("API_BACKEND_URL") or "http://localhost:8000"
