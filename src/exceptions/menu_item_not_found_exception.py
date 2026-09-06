from fastapi import status
from src.exceptions import AppException


class MenuItemNotFoundException(AppException):
    def __init__(self, message: str):
        super().__init__(message, status.HTTP_404_NOT_FOUND)