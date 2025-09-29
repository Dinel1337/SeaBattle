import bcrypt
from ...core.repositories import UserRepository
from ...core.schemas import UserCreate, UserInDB, UserDelete
from ...core.exceptions import UserNotFoundExсeption, UserErrorCreateExсeption, UserEmailExistsExсeption, UserBadParametrError
from ...core.enum import OperationUserStatus
from ...core import crypt_pass
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
        
        password_hash = crypt_pass(user_create.password)

        user = await self.repository.create_user({
            "email": user_create.email,
            "username": user_create.username,
            "password_hash": password_hash
        })

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
            