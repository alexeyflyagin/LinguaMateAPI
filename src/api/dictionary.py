from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query
from starlette import status

from src.api.exceptions import InvalidTokenHTTPException, InternalServerHTTPException
from src.di.app_container import di
from src.models.phrase import GetPhrasesData
from src.models.word import AddWordResponse, AddWordData, AddWordsResponse, AddWordsData, WordEntity, GetWordsResponse, \
    GetWordFlowResponse
from src.services.base.word_service_base import WordService
from src.services.exceptions.service import InvalidTokenError, ServiceError, NotUniqueError, NotFoundError

router = APIRouter(
    prefix="/{token}/dictionary",
    tags=["Dictionary"],
)


@router.post("/addWord", response_model=AddWordResponse)
async def add_phrase(
        token: UUID,
        data: AddWordData,
        word_service: WordService = Depends(lambda: di.services.word_service())
) -> AddWordResponse:
    try:
        return await word_service.add_word(token, data)
    except NotUniqueError:
        raise HTTPException(status.HTTP_409_CONFLICT, detail="This word already exists.")
    except InvalidTokenError:
        raise InvalidTokenHTTPException()
    except ServiceError:
        raise InternalServerHTTPException()


@router.post("/addWords/", response_model=AddWordsResponse)
async def add_words(
        token: UUID,
        data: AddWordsData,
        word_service: WordService = Depends(lambda: di.services.word_service())
) -> AddWordsResponse:
    try:
        return await word_service.add_words(token, data)
    except InvalidTokenError:
        raise InvalidTokenHTTPException()
    except ServiceError:
        raise InternalServerHTTPException()


@router.get("/getWordById", response_model=WordEntity)
async def get_word_by_id(
        token: UUID,
        word_id: int,
        word_service: WordService = Depends(lambda: di.services.word_service())
) -> WordEntity:
    try:
        return await word_service.get_word_by_id(token, word_id)
    except NotFoundError:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="The word not found.")
    except InvalidTokenError:
        raise InvalidTokenHTTPException()
    except ServiceError:
        raise InternalServerHTTPException()


@router.get("/getWords", response_model=GetWordsResponse)
async def get_words(
        token: UUID,
        data: Annotated[GetPhrasesData, Query()],
        word_service: WordService = Depends(lambda: di.services.word_service())
) -> GetWordsResponse:
    try:
        return await word_service.get_words(token, data)
    except InvalidTokenError:
        raise InvalidTokenHTTPException()
    except ServiceError:
        raise InternalServerHTTPException()


@router.get("/getWordFlow", response_model=GetWordFlowResponse)
async def get_word_flow(
        token: UUID,
        word_service: WordService = Depends(lambda: di.services.word_service())
) -> GetWordFlowResponse:
    try:
        res = await word_service.get_word_flow(token)
        return res
    except NotFoundError:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="The dictionary is empty.")
    except InvalidTokenError:
        raise InvalidTokenHTTPException()
    except ServiceError:
        raise InternalServerHTTPException()
