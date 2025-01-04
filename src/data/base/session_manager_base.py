import logging
from abc import ABC

from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession, create_async_engine


class SessionManager(ABC):

    def __init__(self, url):
        self._engine = create_async_engine(url)
        self._session_maker = async_sessionmaker(bind=self._engine)

    def get_session(self) -> AsyncSession:
        return self._session_maker()

    async def disconnect(self):
        await self._engine.dispose()
        logging.info("The database connection is disconnected.")
