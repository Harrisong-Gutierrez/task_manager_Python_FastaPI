from fastapi import APIRouter, Depends, HTTPException

from app.core.auth import get_current_user
from app.infra.repositories.user_repository import UserRepository
from app.domain.models import User
from typing import List

from app.services.user_service import UserService

router = APIRouter(prefix="/users", tags=["users"])


def get_user_service():
    repository = UserRepository()
    return UserService(repository)


@router.get("/public", response_model=List[User])
async def get_users_public(service: UserService = Depends(get_user_service)):
    try:
        return service.get_all_users()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
