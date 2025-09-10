from app.infra.repositories.user_repository import UserRepository
from app.domain.models import User, UserCreate
from app.core.security import verify_password, create_access_token
from datetime import timedelta
from app.core.config import settings
from typing import Optional


class AuthService:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    def authenticate_user(self, email: str, password: str) -> Optional[User]:
        # Obtenemos el usuario por email
        user = self.user_repository.get_by_email(email)
        if not user:
            return None

        # Obtenemos la contraseña hasheada directamente desde el repositorio
        hashed_password = self.user_repository.get_password_hash(email)
        if not hashed_password:
            return None

        # Verificamos la contraseña
        if not verify_password(password, hashed_password):
            return None

        return user

    def create_user(self, user: UserCreate) -> User:

        existing_user = self.user_repository.get_by_email(user.email)
        if existing_user:
            raise ValueError("User already exists")

        return self.user_repository.create(user)

    def create_access_token(self, email: str) -> str:
        access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        return create_access_token(
            data={"sub": email}, expires_delta=access_token_expires
        )

    def get_user_by_email(self, email: str) -> Optional[User]:
        return self.user_repository.get_by_email(email)
