from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession
from ..models import User
import logging

logger = logging.getLogger(__name__)

class UserRepository():
    def __init__(self, session: AsyncSession):
        self.session = session
        
    async def get_by_id(self, user_id: int) -> User | None:
        result = await self.session.execute(select(User).where(User.id == user_id))
        return result.scalar_one_or_none()
    
    async def get_by_email(self, user_email: str) -> User | None:
        result = await self.session.execute(select(User).where(User.email == user_email))
        return result.scalar_one_or_none()
    
    async def get_by_username(self, username: str) -> User | None:
        result = await self.session.execute(select(User).where(User.username == username))
        return result.scalar_one_or_none()
    
    async def create_user(self, data: dict) -> User | bool:
        try:
            user = User(**data)
            self.session.add(user)
            await self.session.commit()
            await self.session.refresh(user)
            return user
        except:
            return False

    async def delete_user_in_base(self, user_id: int) -> bool:
        try:
            result = await self.session.execute(delete(User).where(User.id == user_id))
            await self.session.commit()
            return result.rowcount > 0
        except:
            return False