from fastapi import status
from src.exceptions.app_exception import AppException


class OrderCancellationException(AppException):
    def __init__(self, message: str):
        super().__init__(message, status.HTTP_409_CONFLICT)
