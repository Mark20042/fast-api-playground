from motor.motor_asyncio import AsyncIOMotorClient
from config.config import settings


client = AsyncIOMotorClient(settings.mongodb_url)


db = client[settings.database_name]


async def ping_db():
    try:
        await client.admin.command('ping')
        print("Successfully connected to MongoDB!")
    except Exception as e:
        print(f"Failed to connect to MongoDB: {e}")