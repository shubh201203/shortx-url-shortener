import logging
import time
import asyncio
from typing import Callable
from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
from .redis import redis_client

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler()]
)
logger = logging.getLogger("shortx")

class LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        start_time = time.time()
        
        request.state.cache_hit = False 
        
        response = await call_next(request)
        
        process_time = (time.time() - start_time) * 1000
        cache_status = "HIT" if getattr(request.state, "cache_hit", False) else "MISS"
        
        path = request.url.path
        if path.startswith("/r/"):
            logger.info(f"{request.method} {path} | status={response.status_code} | latency={process_time:.2f}ms | cache={cache_status}")
            
            # Fire and forget Redis metric counters (observability gold without slowing down redirects)
            asyncio.create_task(redis_client.incr("metrics:total_redirects"))
            if cache_status == "HIT":
                asyncio.create_task(redis_client.incr("metrics:cache_hits"))
            else:
                asyncio.create_task(redis_client.incr("metrics:cache_misses"))
        else:
            if path != "/health":
                logger.info(f"{request.method} {path} | status={response.status_code} | latency={process_time:.2f}ms")
            
            if response.status_code == 429:
                asyncio.create_task(redis_client.incr("metrics:rate_limited"))
                
        return response
