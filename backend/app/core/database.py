from motor.motor_asyncio import AsyncIOMotorClient
from .config import settings

class MongoDB:
    client: AsyncIOMotorClient = None
    db = None

db = MongoDB()

async def connect_to_mongo():
    db.client = AsyncIOMotorClient(settings.MONGODB_URL)
    db.db = db.client[settings.DATABASE_NAME]
    
    # Ensure critical indexes as per architecture plan
    await db.db.urls.create_index("short_code", unique=True)
    await db.db.urls.create_index("user_id")
    await db.db.urls.create_index("created_at")
    await db.db.analytics.create_index("short_code")

async def close_mongo_connection():
    if db.client:
        db.client.close()
