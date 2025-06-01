import os

from dotenv import load_dotenv
from pymongo import AsyncMongoClient

load_dotenv()

client = AsyncMongoClient(os.getenv("MONGO_DB_URI"))
db = client[str(os.getenv("MONGO_DB_NAME"))]
