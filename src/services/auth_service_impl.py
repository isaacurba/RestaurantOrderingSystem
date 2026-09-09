from src.exceptions.invalid_credentials_exception import InvalidCredentialException
from src.exceptions.user_not_found_exception import UserNotFoundException
from src.schemas.user import UserLogin, UserResponse, UserCreate, TokenResponse
from src.exceptions.user_already_exist_exception import UserAlreadyExistsException
from src.services.auth_service import AuthService
from src.utils.mapper import Mapper
from src.utils.jwt import create_access_token


class AuthServiceImpl(AuthService):

    def __init__(self, repository):
        self.repository = repository

    def register(self, user_data: UserCreate) -> UserResponse:
        existing_user = self.repository.find_by_email(user_data.email)
        if existing_user is not None:
            raise UserAlreadyExistsException(f"user with email {user_data.email} already exists")

        user = Mapper.map(self, user_data)
        saved_user = self.repository.save(user)
        return UserResponse.model_validate(saved_user)

    def login(self, user_data: UserLogin) -> TokenResponse:
        existing_user = self.repository.find_by_email(user_data.email)
        if existing_user is None:
            raise UserNotFoundException(f"user with email {user_data.email} does not exist")
        if existing_user.password != user_data.password:
            raise InvalidCredentialException("Invalid credentials")
        existing_user.is_active = True
        saved_user = self.repository.save(existing_user)

        token = create_access_token(saved_user.id)
        return TokenResponse(access_token=token, token_type="bearer")