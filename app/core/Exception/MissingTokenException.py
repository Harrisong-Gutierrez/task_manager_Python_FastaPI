
from fastapi import status

from app.core.Exception.CustomException import CustomException


class MissingTokenException(CustomException):
    """Token no proporcionado"""

    def __init__(self):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Token de autenticación no proporcionado",
            headers={"WWW-Authenticate": "Bearer"},
            error_code="missing_token",
        )
