from dependency_injector import containers, providers

from src.services.auth_service import AuthServiceImpl
from src.services.phrase_service import PhraseServiceImpl


class ServiceContainer(containers.DeclarativeContainer):
    config = providers.Configuration()
    data_container = providers.DependenciesContainer()

    auth_service = providers.Factory(
        AuthServiceImpl,
        session_manager=data_container.session_manager,
        bot_key=config.BOT_KEY,
    )

    phrase_service = providers.Factory(
        PhraseServiceImpl,
        session_manager=data_container.session_manager,
    )
