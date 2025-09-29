from dotenv import load_dotenv
load_dotenv()
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
import os
from collections.abc import AsyncGenerator
from backend.config import ECHO
from .base import Base

DATABASE = os.getenv('DATABASE_URL').strip(' "\'').lower()

engine = create_async_engine(DATABASE, echo=ECHO)

AsyncSessionLocal = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False
)

async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as session:
        yield session
        
async def init_db():
    async with engine.begin() as conn:
         await conn.run_sync(Base.metadata.create_all)
        