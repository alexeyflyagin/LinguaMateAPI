from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status

from src.api.exceptions import InternalServerHTTPException
from src.di.app_container import di
from src.services.exceptions.service import AccountNotFound, ServiceError, AccountAlreadyExistsError
from src.models.auth import AuthData, AuthResponse, SignupData, CheckTokenResponse
from src.services.base.auth_service_base import AuthService

router = APIRouter(
    tags=['Authorization']
)


@router.get("/{token}/checkToken/", response_model=CheckTokenResponse)
async def check_token(
        token: UUID,
        auth_service: AuthService = Depends(lambda: di.services.auth_service())
) -> CheckTokenResponse:
    try:
        return await auth_service.check_token(token)
    except ServiceError:
        raise InternalServerHTTPException()


@router.post("/auth/", response_model=AuthResponse)
async def auth(
        auth_data: AuthData,
        auth_service: AuthService = Depends(lambda: di.services.auth_service())
) -> AuthResponse:
    try:
        return await auth_service.auth(auth_data)
    except AccountNotFound:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="The account was not found.")
    except ServiceError:
        raise InternalServerHTTPException()


@router.post("/signup/")
async def sign_up(
        signup_data: SignupData,
        auth_service: AuthService = Depends(lambda: di.services.auth_service())
):
    try:
        await auth_service.signup(signup_data)
    except AccountAlreadyExistsError:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail="Account with this phone number already exists.")
    except ServiceError:
        raise InternalServerHTTPException()
