from uuid import UUID

from fastapi import APIRouter, Depends

from src.api.exceptions import InvalidTokenHTTPException, InternalServerHTTPException
from src.di.app_container import di
from src.models.account import AccountInfoResponse
from src.services.base.account_service_base import AccountService
from src.services.exceptions.service import InvalidTokenError, ServiceError

router = APIRouter(
    tags=['Account'],
    prefix="/{token}/account"
)


@router.get('/getInfo', response_model=AccountInfoResponse)
async def get_info(
        token: UUID,
        account_service: AccountService = Depends(lambda: di.services.account_service()),
) -> AccountInfoResponse:
    try:
        return await account_service.get_info(token)
    except InvalidTokenError:
        raise InvalidTokenHTTPException()
    except ServiceError:
        raise InternalServerHTTPException()
