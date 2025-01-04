from abc import ABC

from src.data.base.session_manager_base import SessionManager
from src.models.auth_models import AuthData, AuthResponse, SignupData


class AuthService(ABC):

    def __init__(self,session_manager: SessionManager):
        self._session_manager = session_manager

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
