from fastapi import HTTPException
from ..enum import ErrorUser

class AppException(HTTPException):
    def __init__(
        self,
        status_code: int,
        error_code: ErrorUser | None = None,
        message: str | None = None,
        details: dict | None = None
    ):
        super().__init__(
            status_code=status_code,
            detail={
                'error_code': error_code,
                'message': message,  # Основное сообщение
                'details': details or {}  # Дополнительные детали
            }
        )