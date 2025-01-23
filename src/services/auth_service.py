import logging
import uuid
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession

from src.dao import dao_account, dao_session
from src.data.base.session_manager_base import SessionManager
from src.services.exceptions.service import ServiceError, AccountNotFound, TokenGenerationError, \
    AccountAlreadyExistsError, AccessError
from src.models.auth import AuthData, AuthResponse, SignupData, CheckTokenResponse
from src.services.base.auth_service_base import AuthService
from src.services.utils import raise_exception_if_none, raise_exception_if_not_none


class AuthServiceImpl(AuthService):

    def __init__(self, session_manager: SessionManager, trusted_key: str):
        self.trusted_key = UUID(trusted_key)
        super().__init__(session_manager)

    @staticmethod
    async def __generate_token(s: AsyncSession) -> UUID:
        for i in range(300):
            new_token = uuid.uuid4()
            account = await dao_session.get_by_token(s, new_token)
            if not account:
                return new_token
        raise TokenGenerationError()

    async def auth(
            self,
            trusted_key: UUID,
            auth_data: AuthData
    ) -> AuthResponse:
        try:
            async with self._session_manager.get_session() as s:
                if self.trusted_key != trusted_key:
                    raise AccessError('The trusted key is invalid.')
                account = await dao_account.get_by_phone_number(s, auth_data.phone_number)
                raise_exception_if_none(account, e=AccountNotFound())

                new_token = await self.__generate_token(s)
                new_session = await dao_session.create(s, account.id, new_token)
                s.add(new_session)

                res = AuthResponse(account_id=account.id, token=new_token, nickname=account.nickname)
                await s.commit()
                return res
        except (AccountNotFound, AccessError) as e:
            logging.debug(e)
            raise
        except TokenGenerationError as e:
            logging.critical(e)
            raise ServiceError()
        except Exception as e:
            logging.error(e)
            raise ServiceError()

    async def signup(
            self,
            trusted_key: UUID,
            signup_data: SignupData
    ):
        try:
            async with self._session_manager.get_session() as s:
                if self.trusted_key != trusted_key:
                    raise AccessError('The trusted key is invalid.')
                account = await dao_account.get_by_phone_number(s, signup_data.phone_number)
                raise_exception_if_not_none(account, e=AccountAlreadyExistsError())
                account = await dao_account.create(
                    s, phone_number=signup_data.phone_number,
                    nickname=signup_data.nickname
                )
                s.add(account)
                await s.commit()
        except (AccountAlreadyExistsError, AccessError) as e:
            logging.debug(e)
            raise
        except Exception as e:
            logging.error(e)
            raise ServiceError()

    async def check_token(self, trusted_key: UUID, token: UUID) -> CheckTokenResponse:
        try:
            async with self._session_manager.get_session() as s:
                if self.trusted_key != trusted_key:
                    raise AccessError('The trusted key is invalid.')
                account = await dao_session.get_by_token(s, token)
                is_valid = True if account else False
                return CheckTokenResponse(is_valid=is_valid)
        except AccessError as e:
            logging.debug(e)
            raise
        except Exception as e:
            logging.error(e)
            raise ServiceError()
