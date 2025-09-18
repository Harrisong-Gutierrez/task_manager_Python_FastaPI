from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt, ExpiredSignatureError
from supabase_auth import User
from app.core.Exception import (
    CustomException,
    ExpiredTokenException,
    InactiveUserException,
    InvalidTokenException,
    MissingTokenException,
    UserNotFoundException,
)
from app.services.user_service import UserService
from app.core.dependencies import get_user_service
from app.core.config import settings
from typing import Optional
import logging
from fastapi import status
from datetime import datetime, timezone

HTTP_401_UNAUTHORIZED = status.HTTP_401_UNAUTHORIZED
HTTP_403_FORBIDDEN = status.HTTP_403_FORBIDDEN
HTTP_500_INTERNAL_SERVER_ERROR = status.HTTP_500_INTERNAL_SERVER_ERROR
HTTP_400_BAD_REQUEST = status.HTTP_400_BAD_REQUEST


logger = logging.getLogger(__name__)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")


def get_current_timestamp() -> int:
    """Obtiene el timestamp actual en UTC"""
    return int(datetime.now(timezone.utc).timestamp())


async def get_current_user(
    token: str = Depends(oauth2_scheme),
    user_service: UserService = Depends(get_user_service),
) -> User:
    """
    Obtiene el usuario actual basado en el token JWT.
    """
    if not token:
        logger.warning("Intento de acceso sin token")
        raise MissingTokenException()

    try:

        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM],
            options={"verify_aud": False, "verify_exp": True},
        )

        email: Optional[str] = payload.get("sub")
        if not email:
            logger.warning("Token sin subject (email)")
            raise InvalidTokenException("Token sin información de usuario válida")

        user = user_service.get_user_by_email(email)
        if not user:
            logger.warning(f"Usuario no encontrado: {email}")
            raise UserNotFoundException(email)

        if hasattr(user, "is_active") and not user.is_active:
            logger.warning(f"Usuario inactivo: {email}")
            raise InactiveUserException(email)

        if hasattr(user, "is_verified") and not user.is_verified:
            logger.warning(f"Usuario no verificado: {email}")
            raise CustomException(
                status_code=HTTP_403_FORBIDDEN,
                detail="Usuario no verificado",
                error_code="user_unverified",
            )

        logger.info(f"Usuario autenticado exitosamente: {email}")
        return user

    except ExpiredSignatureError:
        logger.warning("Token expirado (ExpiredSignatureError)")
        raise ExpiredTokenException()

    except JWTError as e:
        logger.warning(f"Error JWT: {str(e)}")
        raise InvalidTokenException(f"Error en el token: {str(e)}")

    except Exception as e:
        logger.error(f"Error inesperado en autenticación: {str(e)}", exc_info=True)
        raise CustomException(
            status_code=HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error interno del servidor durante la autenticación",
            error_code="internal_error",
        )


async def get_current_user_optional(
    user: Optional[User] = None,
) -> Optional[User]:
    """
    Obtiene el usuario actual si existe, de lo contrario retorna None.
    """

    return user


async def get_current_user_optional_manual(
    token: Optional[str] = Depends(oauth2_scheme),
    user_service: UserService = Depends(get_user_service),
) -> Optional[User]:
    """
    Obtiene el usuario actual si existe, de lo contrario retorna None.
    """
    if not token:
        return None

    try:
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM],
            options={"verify_aud": False, "verify_exp": True},
        )

        email: Optional[str] = payload.get("sub")
        if not email:
            return None

        user = user_service.get_user_by_email(email)
        if not user:
            return None

        if hasattr(user, "is_active") and not user.is_active:
            return None

        return user

    except (JWTError, ExpiredSignatureError):
        return None
    except Exception:
        logger.warning("Error al obtener usuario opcional", exc_info=True)
        return None
