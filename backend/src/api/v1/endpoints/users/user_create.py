from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from backend.src.app.core.database.session import get_db
from backend.src.app.core.schemas import UserCreate, UserInDB
from backend.src.app.services.base import UserService
from backend.src.app.core.repositories import UserRepository
from backend.src.app.core.response import ApiResponse, API_response, construct_meta
from backend.config import USER_PREFIX, USER_TAGS, USER_ROUTER

router = APIRouter(
    prefix=USER_PREFIX,
    tags=[USER_TAGS]
)

@router.post(
    USER_ROUTER,
    summary="Создает пользователя",
    responses={
        status.HTTP_200_OK: {'description': 'User create is success'},
        status.HTTP_400_BAD_REQUEST: {'description': 'Validation error'},
        status.HTTP_409_CONFLICT: {'description': 'Email already exists'},
        status.HTTP_500_INTERNAL_SERVER_ERROR: {'description': 'Server error'}
    },
    response_model=ApiResponse[UserInDB]
    )
async def create_user(
    user_data: UserCreate,
    db: AsyncSession = Depends(get_db)
    ) -> ApiResponse[UserInDB]:
    
    service = UserService(UserRepository(db))
    try:
        user = await service.create_user(user_data)
        meta = construct_meta(reason="Пользователь успешно создан")

        return API_response(status_code= status.HTTP_201_CREATED, success=True, data=user, meta=meta)
    except Exception as e:
        raise