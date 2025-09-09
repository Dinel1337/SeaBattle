from fastapi import status
from typing import Optional
from .app_exception import AppException

class BadParametrError(AppException):
    """Base exception for bad parameter errors."""
    def __init__(
        self,
        parametr: Optional[str] = None,
        message: str = "Bad request parametr",
        error_code: Optional[str] = None,
        details: Optional[dict] = None
    ):
        base_details = {'parameter': parametr}
        if details:
            base_details.update(details)
            
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            error_code=error_code,
            message=message,
            details=base_details
        )
