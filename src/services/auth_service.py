from abc import ABC, abstractmethod

from src.schemas.user import TokenResponse
from src.schemas.user import UserCreate, UserLogin, UserResponse


class AuthService(ABC):

    @abstractmethod
    def register(self, user_data: UserCreate) -> UserResponse:
        pass

    @abstractmethod
    def login(self, user_data: UserLogin) -> TokenResponse:
        pass

