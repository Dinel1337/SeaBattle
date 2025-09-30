from ...core.repositories import UserRepository
from ...core.schemas import UserCreate, UserInDB, UserDelete
from ...core.exceptions import UserNotFoundExсeption, UserErrorCreateExсeption, UserEmailExistsExсeption, UserBadParametrError
from ...core.enum import OperationUserStatus
from ...core.models.user_models import AccessToken, RefreshToken 
from ...core import crypt_pass
from ...auth import create_access_token, create_refresh_token

from datetime import datetime, timedelta, timezone
from backend.config import ACCESS_TOKEN_EXPIRE_MINUTES, REFRESH_TOKEN_EXPIRE_DAYS
import logging
logger = logging.getLogger(__name__)

class UserService:
    def __init__(self, repository: UserRepository):
        self.repository = repository
    
    async def create_user(
        self,
        user_create: UserCreate
        ) -> UserInDB:

        if await self.repository.get_by_email(user_create.email):
            raise UserEmailExistsExсeption(user_create.email)
        
        expires_at_access = datetime.now(timezone.utc) + timedelta(ACCESS_TOKEN_EXPIRE_MINUTES)
        expires_at_refresh = datetime.now(timezone.utc) + timedelta(REFRESH_TOKEN_EXPIRE_DAYS)

        password_hash = crypt_pass(user_create.password)

        user = await self.repository.create_user({
            "email": user_create.email,
            "username": user_create.username,
            "password_hash": password_hash
        })

        access_token = await self.repository.create_token({
            "user_id": user.id,
            "access_token": create_access_token(user.id),
            "expires_at": expires_at_access
        }, AccessToken)

        refresh_token = await self.repository.create_token({
            "user_id": user.id,
            "refresh_token": create_refresh_token(user.id),
            "expires_at": expires_at_access
        }, RefreshToken)

        if not user:
            raise UserErrorCreateExсeption(username=user_create.username)
        
        user_data = vars(user)
        user_data["status_operation"] = OperationUserStatus.CREATED
        
        return UserInDB.model_validate(user_data)
    
    async def delete_user(
        self, 
        user_id: UserDelete
        ) -> UserDelete:
        result = await self.repository.delete_user_in_base(user_id)
        if not result:
            raise UserNotFoundExсeption(user_id)
    
    async def check_user_base(
        self,
        username: str | None = None,
        email: str | None = None
    ) -> UserInDB:
        if not (identifier := email or username):
            raise UserBadParametrError()
        
        method = self.repository.get_by_email if email else self.repository.get_by_username
        user = await method(identifier)
        
        if user:
            return UserInDB.model_validate(user)
        raise UserNotFoundExсeption(identifier)
            