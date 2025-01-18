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
            auth_data: AuthData
    ) -> AuthResponse:
        """
        Create the new session for account.

        :param auth_data:

        :return:

        :raises AccountNotFound:
        :raises ServiceError:
        """

    @abstractmethod
    async def signup(
            self,
            signup_data: SignupData
    ):
        """
        Create the new account.

        :param signup_data:

        :raises AccountAlreadyExistsError:
        :raises ServiceError:
        """

    @abstractmethod
    async def check_token(
            self,
            token: UUID,
    ) -> CheckTokenResponse:
        """
        Check if the token exists.

        :param token:

        :raises ServiceError:
        """
