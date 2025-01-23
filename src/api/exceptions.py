from fastapi import HTTPException, status


class InternalServerHTTPException(HTTPException):

    def __init__(self):
        super().__init__(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal Server Error. Please try again later..."
        )


class InvalidTokenHTTPException(HTTPException):

    def __init__(self):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token."
        )

class InvalidTrustedKeyHTTPException(HTTPException):

    def __init__(self):
        super().__init__(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="The trusted key is invalid."
        )
