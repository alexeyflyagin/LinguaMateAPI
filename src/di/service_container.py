from dependency_injector import containers, providers

from src.services.auth_service import AuthServiceImpl


class ServiceContainer(containers.DeclarativeContainer):
    data_container = providers.DependenciesContainer()

    auth_service = providers.Factory(
        AuthServiceImpl,
        session_manager=data_container.session_manager,
    )
