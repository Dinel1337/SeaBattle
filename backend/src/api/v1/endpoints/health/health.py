from fastapi import APIRouter, status
from backend.config import HEALTH_PREFIX, HEALTH_TAGS

router = APIRouter(
    prefix=HEALTH_PREFIX,
    tags=[HEALTH_TAGS]
)

@router.get(
            '',
            status_code=status.HTTP_200_OK,
            summary='Проверка работоспособности',
            response_description="Возвращает 'ok', если сервер работает"
            )
async def health():
    return{"status" : "ok"}
