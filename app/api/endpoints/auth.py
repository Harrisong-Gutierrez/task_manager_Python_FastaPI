from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.security import OAuth2PasswordRequestForm
from app.api.services.auth_service import AuthService
from app.api.infra.repositories.user_repository import UserRepository
from app.api.domain.models import User, UserCreate, Token

router = APIRouter(prefix="/auth", tags=["auth"])

def get_auth_service():
    repository = UserRepository()
    return AuthService(repository)

@router.post("/register", response_model=User, status_code=status.HTTP_201_CREATED)
async def register(user: UserCreate, service: AuthService = Depends(get_auth_service)):
    try:
        return service.create_user(user)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

@router.post("/token", response_model=Token)
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    service: AuthService = Depends(get_auth_service)
):
    user = service.authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token = service.create_access_token(user.email)
    return {"access_token": access_token, "token_type": "bearer"}