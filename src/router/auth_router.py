from fastapi import APIRouter, status

from src.schemas.user import TokenResponse
from src.controller.auth_controller import AuthController
from src.schemas.user import UserCreate, UserLogin, UserResponse
from src.repositories.user_repository_impl import UserRepositoryImpl
from src.database import SessionLocal
from src.services.auth_service_impl import AuthServiceImpl

router = APIRouter(prefix="/auth", tags=["Auth"])


def get_controller():
    session = SessionLocal()
    repository = UserRepositoryImpl(session)
    service = AuthServiceImpl(repository)
    return AuthController(service)

@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def register(user_data: UserCreate):
    controller = get_controller()
    return controller.register(user_data)

@router.post("/login", response_model=TokenResponse, status_code=status.HTTP_200_OK)
def login(user_data: UserLogin):
    controller = get_controller()
    return controller.login(user_data)