from fastapi import status

from src.exceptions.app_exception import AppException


class OrderNotFoundException(AppException):

    def __init__(self, message: str):
        super().__init__(message, status.HTTP_404_NOT_FOUND)
