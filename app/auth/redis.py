# app/auth/redis.py
from redis.asyncio import Redis
from app.core.config import get_settings

settings = get_settings()

_redis: Redis | None = None

async def get_redis() -> Redis:
    global _redis
    if _redis is None:
        _redis = Redis.from_url(
            settings.REDIS_URL or "redis://localhost",
            decode_responses=True
        )
    return _redis

async def add_to_blacklist(jti: str, exp: int):
    redis = await get_redis()
    await redis.set(f"blacklist:{jti}", "1", ex=exp)

async def is_blacklisted(jti: str) -> bool:
    redis = await get_redis()
    return await redis.exists(f"blacklist:{jti}") == 1