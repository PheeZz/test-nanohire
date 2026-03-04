from .router import router as mock_router
from .hh import hh_router

mock_router.include_router(hh_router)

__all__ = ["mock_router"]
