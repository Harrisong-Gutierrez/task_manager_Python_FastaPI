from app.api.infra.repositories.user_repository import UserRepository
from app.api.domain.models import User, UserCreate
from app.api.core.security import verify_password, create_access_token
from datetime import timedelta
from app.api.core.config import settings
from typing import Optional

class AuthService:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository
    
    def authenticate_user(self, email: str, password: str) -> Optional[User]:
        user = self.user_repository.get_by_email(email)
        if not user:
            return None
        
        # Necesitamos obtener la contraseña hash de la base de datos
        response = self.user_repository.table.select("hashed_password").eq('email', email).execute()
        if not response.data:
            return None
        
        hashed_password = response.data[0]['hashed_password']
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