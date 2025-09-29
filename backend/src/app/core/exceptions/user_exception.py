from .app_exception import AppException
from ..enum import ErrorUser, ErrorEmail
from fastapi import status
from .main_error import BadParametrError
from typing import Optional

suggestions_email = {
    "TYPE_ERROR": "Email должен быть строкой, например 'user@example.com'",
    "VALIDATION_ERROR": "Используйте формат user@example.com",
    "UNKNOWN_ERROR": "Попробуйте другой email или повторите позже"
}

suggestions_password = {
    "TYPE_ERROR": "Пароль должен быть строкой",
    "VALIDATION_ERROR": "Пароль должен содержать минимум 6 символов, включая буквы",
    "UNKNOWN_ERROR": "Попробуйте другой пароль или повторите позже",
    "TOO_SHORT": "Пароль должен содержать минимум 6 символов",
    "TOO_LONG": "Пароль должен содержать максимум 32 символа",
}

class UserNotFoundExсeption(AppException):
    """
    'RU' Принимает на вход значение которое мы не нашли В КОНТЕКСТЕ ПОИСКА В БАЗЕ ДАННЫХ
    """
    def __init__(self, data: int | str):
        super().__init__(
            status_code = status.HTTP_404_NOT_FOUND,
            error_code = ErrorUser.USER_NOT_FOUND.value,
            message = f"User {data} on base not Found",
            details = {data : data,
                       'reason': "Пользователь не найден"}
            )

class UserErrorCreateExсeption(AppException):
    def __init__(self, username: str):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            error_code = ErrorUser.USER_NOT_CREATED.value,
            message = f"User {username} not created",
            details = {
                'username': username,
                'suggestion': 'Try another user class'
            }
        )                     

class UserEmailExistsExсeption(AppException):
    def __init__(self, email: str):
        super().__init__(
            status_code=status.HTTP_409_CONFLICT,
            error_code=ErrorUser.USER_EMAIL_EXIST.value,
            message="Email already exists",
            details={
                'email': email,
                'suggestion': 'Try another email address'
            }
        )

class EmailValidationError(AppException):
    """Ошибка валидации email с детализацией типа ошибки"""
    def __init__(self ,email: str, reason: str, more: Optional[str], error_type: str = "VALIDATION_ERROR"):
        super().__init__(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            error_code=ErrorEmail.INVALID_EMAIL.value,
            message="Некорректный email адрес",
            details={
                "email": email,
                "reason": reason,
                "error_type": error_type,
                "suggestion": self._get_suggestion(error_type, suggestions_email, "Используйте корректный email адресс"),
                'more' : more
            }
        )
    

class PasswordValidationError(AppException):
    """Ошибки валидации password с детализацией типа ошибки"""

    def __init__(self,
                reason: str,
                more: Optional[str],
                error_type: str = "VALIDATION_ERROR"):
        super().__init__(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            error_code=ErrorEmail.INVALID_EMAIL.value,
            message="Некорректный email адрес",
            details={
                "reason": reason,
                "error_type": error_type,
                "suggestion": self._get_suggestion(error_type, suggestions_password, "Используйте другой пароль"),
                'more' : more
            }
        )
        

class UserBadParametrError(BadParametrError):
    def __init__(
        self, parametr: str | None = None):
        super().__init__(
            error_code = ErrorUser.USER_BAD_PARAMETR.value,
            message = "Bad request user parametr, other data",
            parametr = parametr
            )