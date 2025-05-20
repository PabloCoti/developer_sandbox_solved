import os
import redis.asyncio as redis_async

REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))

redis = redis_async.from_url(
    f"redis://{REDIS_HOST}:{REDIS_PORT}", decode_responses=True
)
