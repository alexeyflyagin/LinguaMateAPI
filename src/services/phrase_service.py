import logging
from uuid import UUID

from src.dao import dao_account, dao_session, dao_phrase
from src.data.base.session_manager_base import SessionManager
from src.models.phrase import AddPhraseData, AddPhraseResponse, PhraseEntity, GetPhrasesResponse, GetPhrasesData
from src.services.base.phrase_service_base import PhraseService
from src.services.exceptions.service import ServiceError, InvalidTokenError, NotUniqueError, NotFoundError, AccessError
from src.services.utils import raise_exception_if_none, raise_exception_if_not_none


class PhraseServiceImpl(PhraseService):

    def __init__(self, session_manager: SessionManager):
        super().__init__(session_manager)

    async def add_phrase(
            self,
            token: UUID,
            data: AddPhraseData,
    ) -> AddPhraseResponse:
        try:
            async with self._session_manager.get_session() as s:
                session = await dao_session.get_by_token(s, token, block_row=True)
                raise_exception_if_none(session, e=InvalidTokenError())
                account = await dao_account.get_by_id(s, session.account_id, block_row=True)
                exist_phrase = await dao_phrase.get_by_account_id_and_phrase_lower(
                    s, account_id=account.id, phrase_lower=data.phrase.lower())
                raise_exception_if_not_none(exist_phrase, e=NotUniqueError())
                phrase = await dao_phrase.create(
                    s, account_id=account.id, phrase=data.phrase, translations=data.translations)
                res = AddPhraseResponse(id=phrase.id)
                await s.commit()
                return res
        except NotUniqueError as e:
            logging.info(e)
            raise
        except InvalidTokenError as e:
            logging.info(e)
            raise
        except Exception as e:
            logging.error(e)
            raise ServiceError()

    async def get_phrase_by_id(
            self,
            token: UUID,
            phrase_id: int,
    ) -> PhraseEntity:
        try:
            async with self._session_manager.get_session() as s:
                session = await dao_session.get_by_token(s, token)
                raise_exception_if_none(session, e=InvalidTokenError())
                account = await dao_account.get_by_id(s, session.account_id)
                phrase = await dao_phrase.get_by_id(s, id_=phrase_id)
                if phrase is None or phrase.account_id != account.id:
                    raise NotFoundError()
                return PhraseEntity.model_validate(phrase)
        except NotFoundError as e:
            logging.info(e)
            raise
        except InvalidTokenError as e:
            logging.info(e)
            raise
        except Exception as e:
            logging.error(e)
            raise ServiceError()

    async def get_phrases(
            self,
            token: UUID,
            data: GetPhrasesData,
    ) -> GetPhrasesResponse:
        try:
            async with self._session_manager.get_session() as s:
                session = await dao_session.get_by_token(s, token)
                raise_exception_if_none(session, e=InvalidTokenError())
                account = await dao_account.get_by_id(s, session.account_id)
                phrases = await dao_phrase.get_all_by_account_id(s, account_id=account.id, limit=data.limit,
                                                                 page=data.page)
                phrase_entities = [PhraseEntity.model_validate(i) for i in phrases]
                total = await dao_phrase.get_total_count_by_account_id(s, account_id=account.id)
                return GetPhrasesResponse(total=total, offset=data.page, limit=data.limit, phrases=phrase_entities)
        except InvalidTokenError as e:
            logging.info(e)
            raise
        except Exception as e:
            logging.error(e)
            raise ServiceError()
