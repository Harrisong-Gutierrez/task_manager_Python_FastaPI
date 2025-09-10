from sqlalchemy.orm import Session
from app.domain.models import User, UserCreate
from app.infra.database_models import User as UserDB
from app.core.security import get_password_hash
from typing import Optional, List


class UserRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_all(self) -> List[User]:
        try:
            users_db = self.db.query(UserDB).all()
            return [self._map_to_user(user_db) for user_db in users_db]
        except Exception as e:
            self.db.rollback()
            raise e

    def get_by_email(self, email: str) -> Optional[User]:
        try:
            user_db = self.db.query(UserDB).filter(UserDB.email == email).first()
            if user_db:
                return self._map_to_user(user_db)
            return None
        except Exception as e:
            self.db.rollback()
            raise e

    def create(self, user: UserCreate) -> User:
        try:
            hashed_password = get_password_hash(user.password)
            user_db = UserDB(
                email=user.email,
                full_name=user.full_name,
                password=hashed_password,
                is_active=True,
            )
            self.db.add(user_db)
            self.db.commit()
            self.db.refresh(user_db)
            return self._map_to_user(user_db)
        except Exception as e:
            self.db.rollback()
            raise e

    def get_by_id(self, user_id: str) -> Optional[User]:
        try:
            user_db = self.db.query(UserDB).filter(UserDB.id == user_id).first()
            if user_db:
                return self._map_to_user(user_db)
            return None
        except Exception as e:
            self.db.rollback()
            raise e

    def _map_to_user(self, user_db: UserDB) -> User:
        return User(
            id=str(user_db.id),
            email=user_db.email,
            full_name=user_db.full_name,
            is_active=user_db.is_active,
            created_at=user_db.created_at,
            updated_at=user_db.updated_at,
        )

    def get_password_hash(self, email: str) -> Optional[str]:
        try:
            user_db = self.db.query(UserDB).filter(UserDB.email == email).first()
            if user_db:
                return user_db.password
            return None
        except Exception as e:
            self.db.rollback()
            raise e