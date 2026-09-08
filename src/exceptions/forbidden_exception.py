from src.exceptions import AppException
from fastapi import status

class ForbiddenException(AppException):

    def __init__(self, message: str) -> None:
        super().__init__(message, status.HTTP_403_FORBIDDEN)