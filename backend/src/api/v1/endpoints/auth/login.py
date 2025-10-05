from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from backend.config import AUTH_PREFIX, AUTH_ROUTER_LOGIN, AUTH_TAGS, USER_TAGS
from backend.src.app.core.response import ApiResponse
from backend.src.app.core.schemas import UserLoginResponse, UserInDB
from backend.src.app.services.base import UserService
from backend.src.app.core.repositories import UserRepository
from backend.src.app.core.database import get_db

router = APIRouter(
    prefix=AUTH_PREFIX,
    tags=[AUTH_TAGS, USER_TAGS]
)

@router.post(
    AUTH_ROUTER_LOGIN,
    summary="Проверяет пользователя и выдает ему токен и его данные",
    responses={
        status.HTTP_200_OK: {'description': 'User create is success'},
        status.HTTP_400_BAD_REQUEST: {'description': 'Validation error'},
        status.HTTP_409_CONFLICT: {'description': 'Email already exists'},
        status.HTTP_500_INTERNAL_SERVER_ERROR: {'description': 'Server error'}
    },
    response_model=ApiResponse[UserInDB]
)
async def login_user(
    data: UserLoginResponse,
    db: AsyncSession = Depends(get_db)
) -> ApiResponse[UserInDB]:
    service = UserService(UserRepository(db))
    try:
        data.token = service
        user = ...
    except:
        raise ...   