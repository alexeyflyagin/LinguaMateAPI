from abc import ABC, abstractmethod
from uuid import UUID

from src.data.base.session_manager_base import SessionManager
from src.models.auth import AuthData, AuthResponse, SignupData, CheckTokenResponse


class AuthService(ABC):

    def __init__(self, session_manager: SessionManager):
        self._session_manager = session_manager

    @abstractmethod
    async def auth(
            self,
            trusted_key: UUID,
            auth_data: AuthData
    ) -> AuthResponse:
        """
        Create the new session for account.

        :param trusted_key: The secret key to confirm the link between the Telegram bot and the API.
        :param auth_data:

        :return:

        :raises AccountNotFound:
        :raises ServiceError:
        """

    @abstractmethod
    async def signup(
            self,
            trusted_key: UUID,
            signup_data: SignupData
    ):
        """
        Create the new account.

        :param trusted_key: The secret key to confirm the link between the Telegram bot and the API.
        :param signup_data:

        :raises AccessError: If the bot key is invalid.
        :raises AccountAlreadyExistsError:
        :raises ServiceError:
        """

    @abstractmethod
    async def check_token(
            self,
            trusted_key: UUID,
            token: UUID,
    ) -> CheckTokenResponse:
        """
        Check if the token exists.

        :param trusted_key: The secret key to confirm the link between the Telegram bot and the API.
        :param token:

        :raises ServiceError:
        """
