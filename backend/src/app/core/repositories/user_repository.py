from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession
from ..models import User, Base, AccessToken, RefreshToken
from typing import Type 
import logging
from .main_repository import BaseRepository
logger = logging.getLogger(__name__)

class UserRepository:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.UserBase = BaseRepository(session, User)
        self.AccessTokenBase = BaseRepository(session, AccessToken)
        self.RefreshTokenBase = BaseRepository(session, RefreshToken)

    async def get_id_by_username(self, username: str) -> int | None:
        return await self.UserBase.find_scalar_by(User.id, username=username)

    async def get_by_id(self, user_id: int) -> User | None:
        return await self.UserBase.find_one_by(id=user_id)
    
    async def get_by_email(self, user_email: str) -> User | None:
        return await self.UserBase.find_one_by(email=user_email)
    
    async def get_by_username(self, username: str) -> User | None:
        return await self.UserBase.find_one_by(username=username)
    
    async def create_user(self, data: dict) -> User | bool:
        return await self.UserBase.create(data)

    async def create_token(self, data: dict, token_model: Type[Base]) -> Base | bool:
        """
        Создание записи токена в БД

        Параметры:
        - data: Основные данные записи
        - token_model: Модель таблицы БД
        """
        token_repo = BaseRepository(self.session, token_model)
        return await token_repo.create(data)

    async def delete_user_in_base(self, user_id: int) -> bool:
        return await self.UserBase.delete_by_id(user_id)

    # async def get_access_token_by_id(self, user_id: int, token_model: Type[Base]) -> User | None:
    #     token = self.AccessTokenBase.find_one_by(id=user_id)
    #     return 

    async def check_token_info_access_token(self, token: str) -> bool:
        """
        Создание записи токена в БД

        Параметры:
        - token: Полученный токен
        - token_model: Модель таблицы БД
        """
        token_info = await self.AccessTokenBase.find_one_by(access_token=token)
        return token_info is not None