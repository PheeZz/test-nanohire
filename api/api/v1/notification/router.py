from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from utils.dependencies import get_db_session
from .controller import NotificationController
from .schemas import NotificationManagerInfo, NotificationPerManagerResponse

router = APIRouter(prefix="/notification", tags=["notification"])


@router.get("/responses/list")
async def get_responses(
    session: Annotated[AsyncSession, Depends(get_db_session)],
):
    """
    Получить метчинг менеждера и количества новых откликов на его вакансии.
    """
    data = await NotificationController.list_mapping_manager_responses(session=session)

    return NotificationPerManagerResponse(
        notifications=[
            NotificationManagerInfo(
                manager_name=m["name"], notifications_count=m["count"]
            )
            for m in data.values()
        ]
    )
