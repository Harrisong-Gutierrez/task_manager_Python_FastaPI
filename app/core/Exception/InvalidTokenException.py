from app.core.Exception.CustomException import CustomException
from fastapi import status


class InvalidTokenException(CustomException):
    """Token inválido o malformado"""

    def __init__(self, detail: str = "Token inválido o malformado"):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=detail,
            headers={"WWW-Authenticate": 'Bearer error="invalid_token"'},
            error_code="invalid_token",
        )
