from pydantic import BaseModel, field_validator, ConfigDict, Field

from src.checks import validate_not_empty_str, validate_not_empty


class AddPhraseData(BaseModel):
    phrase: str
    translations: list[str]

    @field_validator('phrase')
    def check_phrase_not_empty(cls, v: str):
        validate_not_empty_str(v, 'phrase')
        return v

    @field_validator('translations')
    def check_translation_not_empty(cls, v: list[str]):
        validate_not_empty(v, 'translations')
        return v


class AddPhraseResponse(BaseModel):
    id: int


class PhraseEntity(BaseModel):
    id: int
    account_id: int
    phrase: str
    phrase_lower: str
    translations: list[str]

    class Config:
        from_attributes = True


class GetPhrasesData(BaseModel):
    page: int = Field(1, ge=1)
    limit: int = Field(10, ge=1, le=100)


class GetPhrasesResponse(BaseModel):
    total: int
    offset: int
    limit: int
    phrases: list[PhraseEntity]
