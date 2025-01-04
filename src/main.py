from contextlib import asynccontextmanager

from fastapi import FastAPI

from src.api import auth


@asynccontextmanager
async def lifespan_handler(app):
    yield
    await auth.di.data.session_manager.disconnect()


app = FastAPI(
    lifespan=lifespan_handler
)

app.include_router(auth.router)
