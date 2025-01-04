from src.services.exceptions.base import LinguaMateAPIException


class ServiceError(LinguaMateAPIException):
    pass

class AccountNotFound(LinguaMateAPIException):
    pass

class AccountAlreadyExistsError(LinguaMateAPIException):
    pass

class TokenGenerationError(LinguaMateAPIException):
    pass
