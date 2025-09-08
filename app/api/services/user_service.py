from app.api.infra.repositories.user_repository import UserRepository
from app.api.domain.models import User
from typing import List, Optional

class UserService:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository
    
    def get_all_users(self) -> List[User]:
        return self.user_repository.get_all()
    
    def get_user_by_id(self, user_id: str) -> Optional[User]:
        return self.user_repository.get_by_id(user_id)
    
    def get_user_by_email(self, email: str) -> Optional[User]:
        return self.user_repository.get_by_email(email)
    
    def create_user(self, user_data: dict) -> User:
        return self.user_repository.create(user_data)