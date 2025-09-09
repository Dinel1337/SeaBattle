from fastapi import FastAPI
from .handler import app_exception_handler, general_exception_handler
from ..exceptions import AppException

def setup_exception_handlers(app: FastAPI) -> None:
    """Регистрирует ошибку, которая наследуется от AppException"""
    app.exception_handler(AppException)(app_exception_handler)
    app.exception_handler(Exception)(general_exception_handler)