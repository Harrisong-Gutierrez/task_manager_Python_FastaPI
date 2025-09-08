from app.api.infra.database import db
from app.api.domain.models import User, UserCreate
from app.api.core.security import get_password_hash
from typing import Optional
from typing import List

class UserRepository:
    def __init__(self):
        self.table = db.get_client().table('users')

    def get_all(self) -> List[User]:
        response = self.table.select("*").execute()
        return [User(
            id=str(user_data['id']),
            email=user_data['email'],
            full_name=user_data['full_name'],
            is_active=user_data['is_active'],
            created_at=user_data['created_at'],
            updated_at=user_data.get('updated_at')
        ) for user_data in response.data] if response.data else []
    def get_by_email(self, email: str) -> Optional[User]:
        response = self.table.select("*").eq('email', email).execute()
        if response.data:
            user_data = response.data[0]
            return User(
                id=str(user_data['id']),
                email=user_data['email'],
                full_name=user_data['full_name'],
                is_active=user_data['is_active'],
                created_at=user_data['created_at'],
                updated_at=user_data.get('updated_at')
            )
        return None
    
    def create(self, user: UserCreate) -> User:
        hashed_password = get_password_hash(user.password)
        user_data = {
            "email": user.email,
            "full_name": user.full_name,
            "hashed_password": hashed_password,
            "is_active": True
        }
        response = self.table.insert(user_data).execute()
        created_user = response.data[0]
        return User(
            id=str(created_user['id']),
            email=created_user['email'],
            full_name=created_user['full_name'],
            is_active=created_user['is_active'],
            created_at=created_user['created_at'],
            updated_at=created_user.get('updated_at')
        )
    
    def get_by_id(self, user_id: str) -> Optional[User]:
        response = self.table.select("*").eq('id', user_id).execute()
        if response.data:
            user_data = response.data[0]
            return User(
                id=str(user_data['id']),
                email=user_data['email'],
                full_name=user_data['full_name'],
                is_active=user_data['is_active'],
                created_at=user_data['created_at'],
                updated_at=user_data.get('updated_at')
            )
        return None