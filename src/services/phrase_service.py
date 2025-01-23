import logging
from uuid import UUID

from src.dao import dao_account, dao_session, dao_phrase
from src.data.base.session_manager_base import SessionManager
from src.models.phrase import AddPhraseData, AddPhraseResponse, PhraseEntity, GetPhrasesResponse, GetPhrasesData, \
    AddPhrasesData, AddPhrasesResponse, GetFlowPhraseResponse
from src.services.base.phrase_service_base import PhraseService
from src.services.exceptions.service import ServiceError, InvalidTokenError, NotUniqueError, NotFoundError
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
        except (InvalidTokenError, NotUniqueError) as e:
            logging.debug(e)
            raise
        except Exception as e:
            logging.error(e)
            raise ServiceError()

    async def add_phrases(
            self,
            token: UUID,
            data: AddPhrasesData,
    ) -> AddPhrasesResponse:
        try:
            async with self._session_manager.get_session() as s:
                session = await dao_session.get_by_token(s, token, block_row=True)
                raise_exception_if_none(session, e=InvalidTokenError())
                account = await dao_account.get_by_id(s, session.account_id, block_row=True)
                already_exists: list[str] = []
                added_phrase_ids: dict[str, int] = {}
                for phrase_data in data.phrases:
                    exist_phrase = await dao_phrase.get_by_account_id_and_phrase_lower(
                        s, account_id=account.id, phrase_lower=phrase_data.phrase.lower())
                    if exist_phrase:
                        already_exists.append(phrase_data.phrase)
                        continue
                    phrase = await dao_phrase.create(
                        s, account_id=account.id, phrase=phrase_data.phrase, translations=phrase_data.translations)
                    added_phrase_ids[phrase.phrase] = phrase.id
                res = AddPhrasesResponse(added_ids=added_phrase_ids, already_exists=already_exists)
                await s.commit()
                return res
        except InvalidTokenError as e:
            logging.debug(e)
            raise
        except Exception as e:
            logging.debug(e)
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
                phrase = await dao_phrase.get_by_id_and_account_id(s, id_=phrase_id, account_id=account.id)
                raise_exception_if_none(phrase, e=NotFoundError("The phrase was not found in the phrasebook"))
                return PhraseEntity.model_validate(phrase)
        except (InvalidTokenError, NotFoundError) as e:
            logging.debug(e)
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
            logging.debug(e)
            raise
        except Exception as e:
            logging.error(e)
            raise ServiceError()

    async def get_flow_phrase(self, token: UUID) -> GetFlowPhraseResponse:
        try:
            async with self._session_manager.get_session() as s:
                session = await dao_session.get_by_token(s, token)
                raise_exception_if_none(session, e=InvalidTokenError())
                account = await dao_account.get_by_id(s, session.account_id)
                phrase = await dao_phrase.get_random_one_by_account_id(s, account_id=account.id)
                raise_exception_if_none(session, e=NotFoundError(f"A phrasebook (account_id={account.id}) is empty"))
                return GetFlowPhraseResponse(phrase=PhraseEntity.model_validate(phrase))
        except (InvalidTokenError, NotFoundError) as e:
            logging.debug(e)
            raise
        except Exception as e:
            logging.error(e)
            raise ServiceError()
