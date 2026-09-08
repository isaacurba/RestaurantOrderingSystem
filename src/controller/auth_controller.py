from src.schemas.user import TokenResponse
from src.schemas.user import UserCreate, UserLogin, UserResponse
from src.services.auth_service import AuthService


class AuthController:

    def __init__(self, service: AuthService):
        self.service = service

    def register(self, user_data: UserCreate) -> UserResponse:
        return self.service.register(user_data)

    def login(self, user_data: UserLogin) -> TokenResponse:
        return self.service.login(user_data)