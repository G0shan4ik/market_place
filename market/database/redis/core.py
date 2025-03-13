from redis.asyncio import Redis
from os import getenv

REDIS_HOST = getenv('REDIS_HOST', None)
REDIS_PORT = int(getenv('REDIS_PORT', 0))
REDIS_USER = getenv('REDIS_USER', None) or None
REDIS_PASSWORD = getenv('REDIS_PASSWORD', None) or None
redis_client = Redis(
    host=REDIS_HOST,
    port=REDIS_PORT,
    username=REDIS_USER,
    password=REDIS_PASSWORD
)


__all__ = [
    'redis_client'
]