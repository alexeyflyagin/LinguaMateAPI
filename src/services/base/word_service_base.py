from abc import ABC, abstractmethod
from uuid import UUID

from src.data.base.session_manager_base import SessionManager
from src.models.word import AddWordData, AddWordResponse, AddWordsData, AddWordsResponse, GetWordsResponse, \
    GetWordsData, GetWordFlowResponse


class WordService(ABC):

    def __init__(self, session_manager: SessionManager):
        self._session_manager = session_manager

    @abstractmethod
    async def add_word(
            self,
            token: UUID,
            data: AddWordData,
    ) -> AddWordResponse:
        """
        Add the new word in the dictionary.

        :raises NotUniqueError: If the phrase already exists in the dictionary
        :raises InvalidTokenError:
        :raises ServiceError:
        """

    @abstractmethod
    async def add_words(
            self,
            token: UUID,
            data: AddWordsData,
    ) -> AddWordsResponse:
        """
        Add the list of words in the dictionary (multiple)

        :raises InvalidTokenError:
        :raises ServiceError:
        """

    @abstractmethod
    async def get_word_by_id(
            self,
            token: UUID,
            word_id: int,
    ) -> GetWordsResponse:
        """
        Get the word from the dictionary by `word_id`.

        :raises NotFoundError:
        :raises InvalidTokenError:
        :raises ServiceError:
        """

    @abstractmethod
    async def get_words(
            self,
            token: UUID,
            data: GetWordsData,
    ) -> GetWordsResponse:
        """
        Get the word list from a dictionary.

        :raises InvalidTokenError:
        :raises ServiceError:
        """

    @abstractmethod
    async def get_word_flow(
            self,
            token: UUID
    ) -> GetWordFlowResponse:
        """
        Get a word from a dictionary to memorize.

        :raises NotFoundError: If the dictionary is empty
        :raises InvalidTokenError:
        :raises ServiceError:
        """
