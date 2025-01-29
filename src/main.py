from contextlib import asynccontextmanager

from fastapi import FastAPI

from src.api import auth, phrase, account, dictionary


@asynccontextmanager
async def lifespan_handler(app):
    yield
    await auth.di.data.session_manager().disconnect()


app = FastAPI(
    title='LinguaMateAPI',
    lifespan=lifespan_handler,
    version='0.1.0',
)

app.include_router(auth.router)
app.include_router(account.router)
app.include_router(dictionary.router)
app.include_router(phrase.router)
