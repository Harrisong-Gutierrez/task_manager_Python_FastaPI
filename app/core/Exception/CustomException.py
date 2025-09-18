from fastapi import Depends, HTTPException

from typing import Optional


class CustomException(HTTPException):
    """Excepción base personalizada para errores de autenticación"""

    def __init__(
        self,
        status_code: int,
        detail: str,
        headers: Optional[dict] = None,
        error_code: Optional[str] = None,
    ):
        super().__init__(status_code=status_code, detail=detail, headers=headers)
        self.error_code = error_code
