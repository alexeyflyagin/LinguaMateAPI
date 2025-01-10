from src.services.exceptions.base import LinguaMateAPIException


class ServiceError(LinguaMateAPIException):
    pass

class AccountNotFound(LinguaMateAPIException):
    pass

class AccountAlreadyExistsError(LinguaMateAPIException):
    pass

class InvalidTokenError(LinguaMateAPIException):
    pass

class NotUniqueError(LinguaMateAPIException):
    pass

class NotFoundError(LinguaMateAPIException):
    pass

class AccessError(LinguaMateAPIException):
    pass

class TokenGenerationError(LinguaMateAPIException):
    pass
