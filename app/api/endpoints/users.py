from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.auth import get_current_user
from app.infra.repositories.user_repository import UserRepository
from app.domain.models import User
from typing import List
from app.services.user_service import UserService
from app.infra.database import get_db

router = APIRouter(prefix="/users", tags=["users"])


def get_user_service(db: Session = Depends(get_db)):
    repository = UserRepository(db)
    return UserService(repository)


@router.get("/public", response_model=List[User])
async def get_users_public(service: UserService = Depends(get_user_service)):
    try:
        return service.get_all_users()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
