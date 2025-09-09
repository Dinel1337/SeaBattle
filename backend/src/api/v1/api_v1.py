from fastapi import APIRouter
from .endpoints.users.user_create import router as create_user_router
from .endpoints.users.user_delete import router as delete_user_router
from .endpoints.users.user_check import router as check_user_router
from .endpoints.health.health import router as health_router

def get_all_router() -> APIRouter:
    router = APIRouter()
    #user include ↓
    router.include_router(delete_user_router)
    router.include_router(create_user_router)
    router.include_router(check_user_router)
    #health include ↓
    router.include_router(health_router)
    return router