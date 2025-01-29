from pydantic import BaseModel, field_validator
from pydantic_core.core_schema import ValidationInfo

from src.checks import validate_phone_number, validate_not_empty_str


class AccountInfoResponse(BaseModel):
    account_id: int
    nickname: str
    phone_number: str
    total_phrases: int
    total_words: int

    @field_validator('nickname')
    def validate_nickname(cls, v: str, info: ValidationInfo):
        validate_not_empty_str(v, field_name=info.field_name)
        return v

    @field_validator('phone_number')
    def validate_phone_number(cls, v):
        validate_phone_number(v)
        return v
