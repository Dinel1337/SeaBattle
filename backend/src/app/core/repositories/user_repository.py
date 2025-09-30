from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession
from ..models import User, Base
import logging
import bcrypt

logger = logging.getLogger(__name__)

def hash_password(password: str) -> str:
    """Хэширование пароля"""
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed.decode('utf-8')

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Проверка пароля"""
    return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))

class UserRepository():
    def __init__(self, session: AsyncSession):
        self.session = session
        
    async def get_id_by_username(self, username: str) -> int | None:
        """получение ID пользователя по username"""
        result = await self.session.execute(select(User.id).where(User.username == username))
        return result.scalar_one_or_none()

    async def get_by_id(self, user_id: int) -> User | None:
        """Поиск пользователя по ID"""
        result = await self.session.execute(select(User).where(User.id == user_id))
        return result.scalar_one_or_none()
    
    async def get_by_email(self, user_email: str) -> User | None:
        """Поиск пользователя по email"""
        result = await self.session.execute(select(User).where(User.email == user_email))
        return result.scalar_one_or_none()
    
    async def get_by_username(self, username: str) -> User | None:
        """Поиск пользователя по нику"""
        result = await self.session.execute(select(User).where(User.username == username))
        return result.scalar_one_or_none()
    
    async def create_user(self, data: dict) -> User | bool:
        """Создания пользователя"""
        try:
            user = User(**data)
            self.session.add(user)
            await self.session.commit()
            await self.session.refresh(user)
            return user
        except:
            return False

    async def create_token(self, data:dict, table: Base) -> Base | bool:
        """Создание токенов"""
        try:
            token = table(**data)
            self.session.add(token)
            await self.session.commit()
            await self.session.refresh(token)
            return token
        except:
            return False

    async def delete_user_in_base(self, user_id: int) -> bool:
        """Удаление пользоватея из БД"""
        try:
            result = await self.session.execute(delete(User).where(User.id == user_id))
            await self.session.commit()
            return result.rowcount > 0
        except:
            return False