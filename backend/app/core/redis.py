import redis.asyncio as redis
from .config import settings

# For Upstash or standard Redis
redis_client = redis.from_url(settings.REDIS_URL, decode_responses=True)
