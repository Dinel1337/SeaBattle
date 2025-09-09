from typing import Optional, Generic, TypeVar, Any
from pydantic import BaseModel
from fastapi.responses import JSONResponse

T = TypeVar('T')

class ApiResponse(BaseModel, Generic[T]):
    """
    Стандартная модель ответа API.
    
    Параметры:
    - success: Успех операции (bool)
    - data: Основные данные ответа (опционально, любого типа)
    - error: Сообщение об ошибке (опционально, строка)
    - meta: Мета-данные (опционально, словарь)
    """
    success: bool
    data: Optional[T] = None
    error: Optional[str] = None
    meta: Optional[dict] = None

def API_response(
    status_code: int,
    success: bool,
    data: Optional[Any] = None,
    meta: Optional[dict] = None,
    error: Optional[str] = None
) -> JSONResponse:
    """
    Формирует стандартизированный JSON-ответ для API.

    Параметры:
    - status_code: HTTP статус-код
    - success: Флаг успешности операции
    - data: Основные данные ответа
    - meta: Дополнительные мета-данные
    - error: Текст ошибки (если есть)

    Возвращает:
    - Объект JSONResponse с унифицированной структурой
    """

    response = ApiResponse(
        success=success,
        data=data,
        error=error,
        meta=meta
    )
    
    return JSONResponse(
        status_code=status_code,
        content=response.dict(exclude_none=True)
    )