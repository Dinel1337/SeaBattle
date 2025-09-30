from fastapi import status, APIRouter, Depends, Query
from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from backend.src.app.core.database.session import get_db
from backend.src.app.core.schemas import CheckUser, UserInDB
from backend.src.app.services.base import UserService
from backend.src.app.core.repositories import UserRepository
from backend.src.app.core.response import API_response, construct_meta, ApiResponse
from backend.config import USER_PREFIX, USER_TAGS, USER_ROUTER_CHECK
from datetime import datetime, timezone

router = APIRouter(
    prefix=USER_PREFIX,
    tags=[USER_TAGS]
)

@router.get(
    USER_ROUTER_CHECK,
    summary='Проверяет наличае пользователя',
    response_description="проверяет пользователя в таблице Postgres SQL, вернет http статус и сами данные пользователя в зависимости от роли того кто запрашивает",
        responses={
        status.HTTP_200_OK: {'description': 'user on base'},
        status.HTTP_404_NOT_FOUND: {'description': 'user not found'},
        status.HTTP_500_INTERNAL_SERVER_ERROR: {'description': 'server dead'},
        }
           )
async def check_user(
    params: CheckUser = Depends(),
    db : AsyncSession = Depends(get_db)
    ) -> ApiResponse[UserInDB]:
    service = UserService(UserRepository(db))
    
    try:
        user = await service.check_user_base(username=params.username, email=params.email)
        meta = construct_meta(reason="Пользователь найден")

        return API_response(status_code=status.HTTP_200_OK ,success=True, data=user, meta=meta)
    
    except Exception as e:
        raise