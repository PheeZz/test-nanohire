from .mock import mock_router
from .router import router as v1_router

v1_router.include_router(mock_router)

__all__ = ["v1_router"]
