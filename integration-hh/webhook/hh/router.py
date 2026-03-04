from fastapi import APIRouter
from .schemas import HHNewResponseOrInvitationVacancyWH

router = APIRouter(prefix="/hh", tags=["hh"])


@router.post(path="/", summary="Обработка вебхуков от HeadHunter")
async def handle_hh_webhook(incoming_data: HHNewResponseOrInvitationVacancyWH):

    return {"message": "Вебхук от HeadHunter успешно обработан"}
