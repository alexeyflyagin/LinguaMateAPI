import logging
from uuid import UUID

from src.dao import dao_session, dao_account, dao_word
from src.data.base.session_manager_base import SessionManager
from src.models.word import AddWordData, AddWordResponse, GetWordFlowResponse, GetWordsData, GetWordsResponse, \
    AddWordsData, AddWordsResponse, WordEntity
from src.services.base.word_service_base import WordService
from src.services.exceptions.service import InvalidTokenError, NotUniqueError, ServiceError, NotFoundError
from src.services.utils import raise_exception_if_none, raise_exception_if_not_none


class WordServiceImpl(WordService):

    def __init__(self, session_manager: SessionManager):
        super().__init__(session_manager)

    async def add_word(self, token: UUID, data: AddWordData) -> AddWordResponse:
        try:
            async with self._session_manager.get_session() as s:
                session = await dao_session.get_by_token(s, token, block_row=True)
                raise_exception_if_none(session, e=InvalidTokenError())
                account = await dao_account.get_by_id(s, session.account_id, block_row=True)
                exist_word = await dao_word.get_by_account_id_and_word(s, account_id=account.id, word=data.word)
                raise_exception_if_not_none(exist_word, e=NotUniqueError())
                word = await dao_word.create(s, account_id=account.id, word=data.word, translations=data.translations,
                                             transcription=data.transcription)
                res = AddWordResponse(id=word.id)
                await s.commit()
                return res
        except (InvalidTokenError, NotUniqueError) as e:
            logging.debug(e)
            raise
        except Exception as e:
            logging.error(e)
            raise ServiceError()

    async def add_words(self, token: UUID, data: AddWordsData) -> AddWordsResponse:
        try:
            async with self._session_manager.get_session() as s:
                session = await dao_session.get_by_token(s, token, block_row=True)
                raise_exception_if_none(session, e=InvalidTokenError())
                account = await dao_account.get_by_id(s, session.account_id, block_row=True)
                already_exists: list[str] = []
                added_words_ids: dict[str, int] = {}
                for word_data in data.words:
                    exist_word = await dao_word.get_by_account_id_and_word(
                        s, account_id=account.id, word=word_data.word)
                    if exist_word:
                        already_exists.append(word_data.word)
                        continue
                    word = await dao_word.create(
                        s, account_id=account.id, word=word_data.word, translations=word_data.translations,
                        transcription=word_data.transcription)
                    added_words_ids[word.word] = word.id
                res = AddWordsResponse(added_ids=added_words_ids, already_exists=already_exists)
                await s.commit()
                return res
        except InvalidTokenError as e:
            logging.debug(e)
            raise
        except Exception as e:
            logging.debug(e)
            raise ServiceError()

    async def get_word_by_id(self, token: UUID, word_id: int) -> GetWordsResponse:
        try:
            async with self._session_manager.get_session() as s:
                session = await dao_session.get_by_token(s, token)
                raise_exception_if_none(session, e=InvalidTokenError())
                account = await dao_account.get_by_id(s, session.account_id)
                phrase = await dao_word.get_by_id_and_account_id(s, id_=word_id, account_id=account.id)
                raise_exception_if_none(phrase, e=NotFoundError("The word was not found in the dictionary"))
                return WordEntity.model_validate(phrase)
        except (InvalidTokenError, NotFoundError) as e:
            logging.debug(e)
            raise
        except Exception as e:
            logging.error(e)
            raise ServiceError()

    async def get_words(self, token: UUID, data: GetWordsData) -> GetWordsResponse:
        try:
            async with self._session_manager.get_session() as s:
                session = await dao_session.get_by_token(s, token)
                raise_exception_if_none(session, e=InvalidTokenError())
                account = await dao_account.get_by_id(s, session.account_id)
                words = await dao_word.get_all_by_account_id(s, account_id=account.id, limit=data.limit,
                                                             page=data.page)
                word_entities = [WordEntity.model_validate(i) for i in words]
                total = await dao_word.get_total_count_by_account_id(s, account_id=account.id)
                return GetWordsResponse(total=total, offset=data.page, limit=data.limit, words=word_entities)
        except InvalidTokenError as e:
            logging.debug(e)
            raise
        except Exception as e:
            logging.error(e)
            raise ServiceError()

    async def get_word_flow(self, token: UUID) -> GetWordFlowResponse:
        try:
            async with self._session_manager.get_session() as s:
                session = await dao_session.get_by_token(s, token)
                raise_exception_if_none(session, e=InvalidTokenError())
                account = await dao_account.get_by_id(s, session.account_id)
                word = await dao_word.get_random_one_by_account_id(s, account_id=account.id)
                raise_exception_if_none(word, e=NotFoundError(f"A dictionary (account_id={account.id}) is empty"))
                return GetWordFlowResponse(word=WordEntity.model_validate(word))
        except (InvalidTokenError, NotFoundError) as e:
            logging.debug(e)
            raise
        except Exception as e:
            logging.error(e)
            raise ServiceError()
