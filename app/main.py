from fastapi import FastAPI
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from redis import asyncio as aioredis
from fastapi.staticfiles import StaticFiles

from app.api.endpoints.auth.router import router as auth_router

from app.api.endpoints.hotels.router import router
from app.api.endpoints.bookings.router import router_booking
from app.api.endpoints.tasks.router import router as router_task
from app.api.endpoints.pages.router import router as router_pages
from logging.config import dictConfig
from fastapi import FastAPI

from app.config import log_config

dictConfig(log_config)

app = FastAPI(
    title="Trading App"
)
app.mount("/static", StaticFiles(directory="app/api/endpoints/static"), name="static")

app.include_router(auth_router)

app.include_router(router)
app.include_router(router_booking)
app.include_router(router_task)
app.include_router(router_pages)


@app.on_event("startup")
async def startup_event():
    redis = aioredis.from_url("redis://localhost", encoding="utf8", decode_responses=True)
    FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache")
