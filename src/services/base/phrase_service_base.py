from abc import ABC, abstractmethod
from uuid import UUID

from src.data.base.session_manager_base import SessionManager
from src.models.phrase import AddPhraseData, AddPhraseResponse, GetPhrasesResponse, GetPhrasesData, \
    AddPhrasesData, AddPhrasesResponse, GetFlowPhraseResponse


class PhraseService(ABC):

    def __init__(self, session_manager: SessionManager):
        self._session_manager = session_manager

    @abstractmethod
    async def add_phrase(
            self,
            token: UUID,
            data: AddPhraseData,
    ) -> AddPhraseResponse:
        """
        Add the new phrase in the phrasebook.

        :raises NotUniqueError: If the phrase already exists in the phrasebook
        :raises InvalidTokenError:
        :raises ServiceError:
        """

    @abstractmethod
    async def add_phrases(
            self,
            token: UUID,
            data: AddPhrasesData,
    ) -> AddPhrasesResponse:
        """
        Add the list of phrases in the phrasebook (multiple)

        :raises InvalidTokenError:
        :raises ServiceError:
        """

    @abstractmethod
    async def get_phrase_by_id(
            self,
            token: UUID,
            phrase_id: int,
    ) -> AddPhraseResponse:
        """
        Get the phrase from the phrasebook by `phrase_id`.

        :raises NotFoundError:
        :raises InvalidTokenError:
        :raises ServiceError:
        """

    @abstractmethod
    async def get_phrases(
            self,
            token: UUID,
            data: GetPhrasesData,
    ) -> GetPhrasesResponse:
        """
        Get the phrases list from a phrasebook.

        :raises InvalidTokenError:
        :raises ServiceError:
        """

    @abstractmethod
    async def get_flow_phrase(
            self,
            token: UUID
    ) -> GetFlowPhraseResponse:
        """
        Get a phrase from a phrasebook to memorize.

        :raises NotFoundError: If the phrasebook is empty
        :raises InvalidTokenError:
        :raises ServiceError:
        """
