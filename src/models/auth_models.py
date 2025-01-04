from uuid import UUID

from pydantic import BaseModel, field_validator

from src.checks import validate_phone_number


class SignupData(BaseModel):
    nickname: str
    phone_number: str

    @field_validator('nickname')
    def validate_nickname(cls, v: str):
        if v.strip() == '':
            raise ValueError("The nickname cannot be empty.")
        return v

    @field_validator('phone_number')
    def validate_phone_number(cls, v):
        validate_phone_number(v)
        return v


class AuthData(BaseModel):
    phone_number: str

    @field_validator('phone_number')
    def validate_phone_number(cls, v):
        validate_phone_number(v)
        return v


class AuthResponse(BaseModel):
    account_id: int
    token: UUID
