from fastapi import FastAPI
from server import product_router
from typing import AsyncGenerator, Any
from contextlib import asynccontextmanager

from .db import DATABASE_ENGINE, Base

@asynccontextmanager
async def _lifespan(_:FastAPI) -> AsyncGenerator[None, Any]:
    async with DATABASE_ENGINE.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield

def create_app() -> FastAPI:
    app = FastAPI(lifespan=_lifespan)
    app.include_router(product_router)

    return app