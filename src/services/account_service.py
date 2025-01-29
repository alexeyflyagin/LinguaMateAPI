import logging
from uuid import UUID

from src.dao import dao_account, dao_session, dao_phrase, dao_word
from src.data.base.session_manager_base import SessionManager
from src.models.account import AccountInfoResponse
from src.services.base.account_service_base import AccountService
from src.services.exceptions.service import ServiceError, InvalidTokenError
from src.services.utils import raise_exception_if_none


class AccountServiceImpl(AccountService):

    def __init__(self, session_manager: SessionManager):
        super().__init__(session_manager)

    async def get_info(self, token: UUID) -> AccountInfoResponse:
        try:
            async with self._session_manager.get_session() as s:
                session = await dao_session.get_by_token(s, token)
                raise_exception_if_none(session, e=InvalidTokenError())
                account = await dao_account.get_by_id(s, session.account_id)
                total_phrases = await dao_phrase.get_total_count_by_account_id(s, account_id=account.id)
                total_words = await dao_word.get_total_count_by_account_id(s, account_id=account.id)
                return AccountInfoResponse(
                    account_id=account.id,
                    nickname=account.nickname,
                    phone_number=account.phone_number,
                    total_phrases=total_phrases,
                    total_words=total_words,
                )
        except InvalidTokenError as e:
            logging.debug(e)
            raise
        except Exception as e:
            logging.error(e)
            raise ServiceError()
