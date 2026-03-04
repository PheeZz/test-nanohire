from .auth import auth_router
from .notification import notification_router
from .router import router as api_v1_router

api_v1_router.include_router(auth_router)
api_v1_router.include_router(notification_router)

__all__ = ["api_v1_router"]
