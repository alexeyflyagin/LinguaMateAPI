from abc import ABC, abstractmethod
from uuid import UUID

from src.data.base.session_manager_base import SessionManager
from src.models.phrase import AddPhraseData, AddPhraseResponse, PhraseEntity, GetPhrasesResponse, GetPhrasesData


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

        :param token:
        :param data:

        :return:

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

        :param token:
        :param phrase_id:

        :return:

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

        :param token:
        :param data:

        :return:

        :raises InvalidTokenError:
        :raises ServiceError:
        """
