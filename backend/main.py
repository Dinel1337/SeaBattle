from fastapi import FastAPI
from backend.src.api.v1.api_v1 import get_all_router
from backend.src.app.core.database.session import init_db
from contextlib import asynccontextmanager
from backend.src.app.core.error_handler import setup_exception_handlers
from .config import DEBUG

@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield 
    
app = FastAPI(lifespan=lifespan, debug=DEBUG)

setup_exception_handlers(app)
app.include_router(get_all_router())