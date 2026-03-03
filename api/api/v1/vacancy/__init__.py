from .router import router
from .response import router as response_router

router.include_router(response_router, tags=["vacancy"])

__all__ = ["router"]
