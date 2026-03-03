from fastapi import APIRouter, Depends

from utils.dependencies import verify_service_key

router = APIRouter(prefix="/response", tags=["vacancy responses"])


@router.get(
    "/list",
    summary="Получить отклики на вакансии",
    dependencies=[Depends(verify_service_key)],
)
async def list_responses_by_manager(
    manager_id: str,
):
    """
    Получить отклики на вакансии менеджера.

    - **Ответ**: Список откликов на мои вакансии.
    """

    return {"message": "Получить отклики на мои вакансии"}
