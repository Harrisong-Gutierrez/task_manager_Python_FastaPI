from app.core.Exception.CustomException import CustomException
from fastapi import status


class InactiveUserException(CustomException):
    """Usuario inactivo"""

    def __init__(self, email: str):
        super().__init__(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"Usuario inactivo: {email}",
            error_code="user_inactive",
        )
