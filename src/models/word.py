from pydantic import BaseModel, field_validator, Field
from pydantic_core.core_schema import ValidationInfo

from src.checks import validate_not_empty_str, validate_not_empty


class AddWordData(BaseModel):
    word: str
    translations: list[str]
    transcription: str | None

    @field_validator('word')
    def check_word_not_empty(cls, v: str, info: ValidationInfo):
        validate_not_empty_str(v, info.field_name)
        return v

    @field_validator('transcription')
    def check_transcription_not_empty(cls, v: str | None, info: ValidationInfo):
        if v is not None:
            validate_not_empty_str(v, info.field_name)
        return v

    @field_validator('translations')
    def check_translation_not_empty(cls, v: list[str], info: ValidationInfo):
        validate_not_empty(v, info.field_name)
        return v


class AddWordsData(BaseModel):
    words: list[AddWordData]

    @field_validator('words')
    def check_words_not_empty(cls, v: list[str], info: ValidationInfo):
        validate_not_empty(v, info.field_name)
        return v


class AddWordResponse(BaseModel):
    id: int


class AddWordsResponse(BaseModel):
    added_ids: dict[str, int]
    already_exists: list[str]


class WordEntity(BaseModel):
    id: int
    account_id: int
    word: str
    translations: list[str]
    transcription: str | None

    class Config:
        from_attributes = True


class GetWordsData(BaseModel):
    page: int = Field(1, ge=1)
    limit: int = Field(10, ge=1, le=100)


class GetWordsResponse(BaseModel):
    total: int
    offset: int
    limit: int
    words: list[WordEntity]


class GetWordFlowResponse(BaseModel):
    word: WordEntity
