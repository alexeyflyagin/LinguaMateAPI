from abc import ABC, abstractmethod
from uuid import UUID

from src.data.base.session_manager_base import SessionManager
from src.models.account import AccountInfoResponse
from src.models.auth import AuthData, AuthResponse, SignupData, CheckTokenResponse


class AccountService(ABC):

    def __init__(self, session_manager: SessionManager):
        self._session_manager = session_manager

    @abstractmethod
    async def get_info(
            self,
            token: UUID,
    ) -> AccountInfoResponse:
        """
        Use it to get info about account.

        :param token: The token of the user session (UUID)

        :raises InvalidTokenError:
        :raises ServiceError:
        """
