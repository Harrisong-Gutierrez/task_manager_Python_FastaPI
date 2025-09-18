from app.core.Exception.CustomException import CustomException
from fastapi import status


class UserNotFoundException(CustomException):
    """Usuario no encontrado"""

    def __init__(self, email: str):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Usuario no encontrado: {email}",
            headers={"WWW-Authenticate": 'Bearer error="invalid_token"'},
            error_code="user_not_found",
        )
