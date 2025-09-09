from email_validator import validate_email, EmailNotValidError
from ..exceptions import EmailValidationError
from typing import Any

def validate_email_address(email: Any) -> str:
    """
    Универсальный валидатор email, который обрабатывает:
    - EmailNotValidError (из email-validator)
    - TypeError (если передали не строку)
    - ValueError (некорректный формат)
    - Любые другие ошибки
    """
    if not isinstance(email, str):
        raise EmailValidationError(
            email=email,
            reason="type is not valid, use 'email' format",
            error_type="TYPE_ERROR"
        )
    try:
        validate = validate_email(email)
        return validate.normalized
    
    except EmailNotValidError as e:
        raise EmailValidationError(
            email=email,
            reason="Введите корректный email адрес",
            error_type="VALIDATION_ERROR",
            more=str(e)
        )
    
    except Exception as e:
        raise EmailValidationError(
            email=email,
            reason="Неожиданные ",
            error_type="VALIDATION_ERROR"
        )