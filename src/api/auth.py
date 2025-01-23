from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status

from src.api.exceptions import InternalServerHTTPException, InvalidTrustedKeyHTTPException
from src.di.app_container import di
from src.services.exceptions.service import AccountNotFound, ServiceError, AccountAlreadyExistsError, AccessError
from src.models.auth import AuthData, AuthResponse, SignupData, CheckTokenResponse
from src.services.base.auth_service_base import AuthService

router = APIRouter(
    tags=['Authorization']
)


@router.get("/{trusted_key}/{token}/checkToken/", response_model=CheckTokenResponse)
async def check_token(
        trusted_key: UUID,
        token: UUID,
        auth_service: AuthService = Depends(lambda: di.services.auth_service())
) -> CheckTokenResponse:
    try:
        return await auth_service.check_token(trusted_key, token)
    except AccessError:
        raise InvalidTrustedKeyHTTPException()
    except ServiceError:
        raise InternalServerHTTPException()


@router.post("/{trusted_key}/auth/", response_model=AuthResponse)
async def auth(
        trusted_key: UUID,
        auth_data: AuthData,
        auth_service: AuthService = Depends(lambda: di.services.auth_service())
) -> AuthResponse:
    try:
        return await auth_service.auth(trusted_key, auth_data)
    except AccessError:
        raise InvalidTrustedKeyHTTPException()
    except AccountNotFound:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="The account was not found.")
    except ServiceError:
        raise InternalServerHTTPException()


@router.post("/{trusted_key}/signup/")
async def signup(
        trusted_key: UUID,
        signup_data: SignupData,
        auth_service: AuthService = Depends(lambda: di.services.auth_service())
):
    try:
        await auth_service.signup(trusted_key, signup_data)
    except AccessError:
        raise InvalidTrustedKeyHTTPException()
    except AccountAlreadyExistsError:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail="Account with this phone number already exists.")
    except ServiceError:
        raise InternalServerHTTPException()
