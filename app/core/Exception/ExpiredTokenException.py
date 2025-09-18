from app.core.Exception.CustomException import CustomException
from fastapi import status


class ExpiredTokenException(CustomException):
    """Token expirado"""

    def __init__(self, detail: str = "Token expirado"):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=detail,
            headers={
                "WWW-Authenticate": 'Bearer error="invalid_token", error_description="Token expired"'
            },
            error_code="token_expired",
        )
