from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query
from starlette import status

from src.api.exceptions import TokenInvalidateHTTPException, InternalServerHTTPException
from src.di.app_container import di
from src.models.phrase import AddPhraseResponse, AddPhraseData, PhraseEntity, GetPhrasesResponse, GetPhrasesData
from src.services.base.phrase_service_base import PhraseService
from src.services.exceptions.service import InvalidTokenError, ServiceError, NotUniqueError, NotFoundError

router = APIRouter(
    prefix="/{token}/phrasebook",
    tags=["Phrasebook"],
)


@router.post("/addPhrase", response_model=AddPhraseResponse)
async def add_phrase(
        token: UUID,
        data: AddPhraseData,
        phrase_service: PhraseService = Depends(lambda: di.services.phrase_service())
) -> AddPhraseResponse:
    try:
        response: AddPhraseResponse = await phrase_service.add_phrase(token, data)
        return response
    except NotUniqueError:
        raise HTTPException(status.HTTP_409_CONFLICT, detail="This phrase already exists.")
    except InvalidTokenError:
        raise TokenInvalidateHTTPException()
    except ServiceError:
        raise InternalServerHTTPException()


@router.get("/getPhraseById", response_model=PhraseEntity)
async def get_phrase_by_id(
        token: UUID,
        phrase_id: int,
        phrase_service: PhraseService = Depends(lambda: di.services.phrase_service())
) -> PhraseEntity:
    try:
        response: PhraseEntity = await phrase_service.get_phrase_by_id(token, phrase_id)
        return response
    except NotFoundError:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Phrase not found.")
    except InvalidTokenError:
        raise TokenInvalidateHTTPException()
    except ServiceError:
        raise InternalServerHTTPException()


@router.get("/getPhrases", response_model=GetPhrasesResponse)
async def get_phrases(
        token: UUID,
        data: Annotated[GetPhrasesData, Query()],
        phrase_service: PhraseService = Depends(lambda: di.services.phrase_service())
) -> GetPhrasesResponse:
    try:
        return await phrase_service.get_phrases(token, data)
    except InvalidTokenError:
        raise TokenInvalidateHTTPException()
    except ServiceError:
        raise InternalServerHTTPException()
