from fastapi import Request
from fastapi.responses import JSONResponse
from datetime import datetime
from ..exceptions import AppException
from backend.config import DEBUG

async def app_exception_handler(request: Request, exc: AppException):

    """Обработка ошибок с пользователями"""

    return JSONResponse(
        status_code=exc.status_code,
        content={
            "success": False,
            "error": exc.detail,
            "meta": {
                "timestamp": datetime.utcnow().isoformat(),
                "path": request.url.path
            }
        },
        headers=exc.headers
    )

async def general_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={
            "success": False,
            "error": {
                "code": "INTERNAL_SERVER_ERROR",
                "type": "UnexpectedError",
                "message": "Internal server error",
                "details": str(exc) if DEBUG else None
            },
            "meta": {
                "timestamp": datetime.utcnow().isoformat(),
                "path": request.url.path
            }
        }
    )