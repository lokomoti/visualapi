"""Main entry point for the Visual API application."""

from contextlib import asynccontextmanager

from api.routes import router as api_router
from db import local as db_local
from fastapi import FastAPI
from fastapi_cache import FastAPICache
from fastapi_cache.backends.inmemory import InMemoryBackend


@asynccontextmanager
async def lifespan(_: FastAPI):
    db_local.init_db()
    FastAPICache.init(InMemoryBackend())
    yield


app = FastAPI(
    title="Visual API",
    description="API for querying data from Visual ERP system",
    version="0.0.1",
    lifespan=lifespan,
)
app.include_router(api_router)
