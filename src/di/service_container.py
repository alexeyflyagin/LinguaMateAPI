from dependency_injector import containers, providers

from src.services.account_service import AccountServiceImpl
from src.services.auth_service import AuthServiceImpl
from src.services.phrase_service import PhraseServiceImpl
from src.services.word_service import WordServiceImpl


class ServiceContainer(containers.DeclarativeContainer):
    config = providers.Configuration()
    data_container = providers.DependenciesContainer()

    auth_service = providers.Factory(
        AuthServiceImpl,
        session_manager=data_container.session_manager,
        trusted_key=config.TRUSTED_KEY,
    )

    account_service = providers.Factory(
        AccountServiceImpl,
        session_manager=data_container.session_manager,
    )

    phrase_service = providers.Factory(
        PhraseServiceImpl,
        session_manager=data_container.session_manager,
    )

    word_service = providers.Factory(
        WordServiceImpl,
        session_manager=data_container.session_manager,
    )
