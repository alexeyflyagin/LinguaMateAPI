from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from src.data.base.session_manager_base import SessionManager


class SessionManagerImpl(SessionManager):

    def __init__(self, url: str):
        super().__init__(url)
