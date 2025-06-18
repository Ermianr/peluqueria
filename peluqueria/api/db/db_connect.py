from pymongo import AsyncMongoClient

from peluqueria.settings import Settings

client = AsyncMongoClient(Settings.MONGO_DB_URI)
db = client[Settings.MONGO_DB_NAME]


async def create_indexes() -> None:
    await db["users"].create_index("email", unique=True)
