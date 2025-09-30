from fastapi import APIRouter, Depends, status
from backend.config import USER_PREFIX, USER_TAGS, USER_ROUTER_DELETE
from backend.src.app.core.database.session import get_db
from backend.src.app.services.base import UserService
from backend.src.app.core.repositories import UserRepository
from backend.src.app.core.response import ApiResponse, API_response, construct_meta
from backend.src.app.core.schemas import UserDelete
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter(
    prefix=USER_PREFIX,
    tags=[USER_TAGS]
)

@router.delete(
    USER_ROUTER_DELETE + '/{user_id}',
    summary='Удаляет пользователя',
    response_description="Удаляет пользователя из PostgresSQL в случае успеха вернет ok",
    responses={
        status.HTTP_200_OK: {'description': 'user delete succsess'},
        status.HTTP_404_NOT_FOUND: {'description': 'user not found'},
        status.HTTP_500_INTERNAL_SERVER_ERROR: {'description': 'server dead'},
        }
    )
async def user_delete(
    user_id: int,
    db: AsyncSession = Depends(get_db)
    ) -> ApiResponse[UserDelete]:
    try:
        service = UserService(UserRepository(db))
        await service.delete_user(user_id)

        meta = construct_meta(reason="Пользователь успешно найден")

        return API_response(status_code= status.HTTP_200_OK, success=True, data=user_id, meta=meta)
    except Exception as e:
        raise