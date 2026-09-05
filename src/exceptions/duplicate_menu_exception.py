from fastapi import status

from exceptions import AppException


class DuplicateMenuException(AppException):
    def __init__(self, message: str):
        super().__init__(message, status.HTTP_409_CONFLICT)