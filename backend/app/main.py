from contextlib import asynccontextmanager

import uvicorn

from fastapi import FastAPI
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from redis import asyncio as aioredis  # type: ignore

from app.api.main import api_router
from app.core.config import settings


@asynccontextmanager
async def lifespan(app: FastAPI):
    redis = aioredis.from_url(
        str(settings.REDIS_CACHE_URI),
        encoding="utf8",
        decode_responses=True,
    )
    FastAPICache.init(RedisBackend(redis), prefix="api:cache")
    yield
    await redis.close()


app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    lifespan=lifespan,
)

app.include_router(api_router, prefix=settings.API_V1_STR)

if __name__ == "__main__":
    uvicorn.run(
        app="app.main:app",
        host=settings.HOST_BACKEND,
        port=settings.PORT_BACKEND,
        reload=True,
        workers=1,
    )
