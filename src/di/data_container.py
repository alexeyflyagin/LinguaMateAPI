from dependency_injector import containers, providers

from src.data.session_manager import SessionManagerImpl


class DataContainer(containers.DeclarativeContainer):
    config = providers.Configuration()

    session_manager = providers.Singleton(
        SessionManagerImpl,
        url=config.DB_URL,
    )
