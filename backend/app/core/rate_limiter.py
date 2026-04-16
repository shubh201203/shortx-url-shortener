import time
from fastapi import Request, HTTPException
from .redis import redis_client
from .logging import logger

async def sliding_window_rate_limit(request: Request, limit: int = 100, window: int = 60):
    """
    Sliding window rate limit using Redis Sorted Sets (ZSET).
    Key: rate_limit:{ip}
    Score: timestamp
    Value: unique identifier (timestamp + random mapping)
    """
    ip = request.client.host if request.client else "127.0.0.1"
    key = f"rate_limit:{ip}"
    current_time = time.time()
    window_start = current_time - window

    try:
        pipeline = redis_client.pipeline()
        
        # Remove old requests
        pipeline.zremrangebyscore(key, 0, window_start)
        
        # Add current request
        identifier = f"{current_time}-{id(request)}"
        pipeline.zadd(key, {identifier: current_time})
        
        # Count requests inside the window
        pipeline.zcard(key)
        
        # Update TTL
        pipeline.expire(key, window)
        
        results = await pipeline.execute()
        request_count = results[2]
        
        if request_count > limit:
            raise HTTPException(
                status_code=429,
                detail="Too Many Requests"
            )
    except HTTPException:
        raise
    except Exception as e:
        # Prioritize availability over strict rate limiting
        logger.error(f"Rate Limiter Failure - Failing Open | Error: {e}")
