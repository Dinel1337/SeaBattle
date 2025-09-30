from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession
from ..models import Base
from typing import Generic, TypeVar, Type, Optional, Any
import logging

logger = logging.getLogger(__name__)

T = TypeVar('T', Base)

class BaseRepository(Generic[T]):
    def __init__(self, session: AsyncSession, model: Type[T]):
        self.session = session
        self.model = model
    
    async def find_one_by(self, **filters) -> Optional[T]:
        result = await self.session.execute(
            select(self.model).filter_by(**filters)
        )
        return result.scalar_one_or_none()
    
    async def find_scalar_by(self, column: Any, **filters) -> Optional[Any]:
        result = await self.session.execute(
            select(column).filter_by(**filters)
        )
        return result.scalar_one_or_none()
    
    async def create(self, data: dict) -> T | bool:
        try:
            instance = self.model(**data)
            self.session.add(instance)
            await self.session.commit()
            await self.session.refresh(instance)
            return instance
        except Exception as e:
            logger.error(f"Error creating {self.model.__name__}: {e}")
            await self.session.rollback()
            return False
    
    async def delete_by_id(self, record_id: int) -> bool:
        try:
            result = await self.session.execute(
                delete(self.model).where(self.model.id == record_id)
            )
            await self.session.commit()
            return result.rowcount > 0
        except Exception as e:
            logger.error(f"Error deleting {self.model.__name__}: {e}")
            await self.session.rollback()
            return False