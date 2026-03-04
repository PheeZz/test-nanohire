from .v1 import v1_router
from .router import router as api_router

api_router.include_router(v1_router)

__all__ = ["api_router"]
