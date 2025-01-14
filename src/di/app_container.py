from dependency_injector import containers, providers

from src import config
from src.di.data_container import DataContainer
from src.di.service_container import ServiceContainer


class AppContainer(containers.DeclarativeContainer):
    config = providers.Configuration()

    data = providers.Container(DataContainer, config=config)
    services = providers.Container(ServiceContainer, data_container=data)


di: AppContainer


di = AppContainer()
di.config.DB_URL.from_value(config.DB_URL)
