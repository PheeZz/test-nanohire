from typing import Annotated

from fastapi import APIRouter, Response
from fastapi.params import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from utils.dependencies import get_db_session
from .controller import HHController
from .schemas import HHNewResponseOrInvitationVacancyWH
from fastapi import status

router = APIRouter(prefix="/hh", tags=["hh"])


@router.post(path="/", summary="Обработка вебхуков от HeadHunter")
async def handle_hh_webhook(
    incoming_data: HHNewResponseOrInvitationVacancyWH,
    session: Annotated[AsyncSession, Depends(get_db_session)],
):
    resume = await HHController.get_resume_data(
        resume_id=incoming_data.payload.resume_id
    )

    if not resume:
        # возвращаем 200, чтобы HH не пытался повторить запрос,
        # так как мы уже обработали его, хоть и не смогли получить данные резюме
        return Response(status_code=status.HTTP_200_OK)

    # если уже есть совпадение между этим резюме и вакансией, то не нужно его обрабатывать повторно
    if await HHController.is_matching_exist(
        resume_id=incoming_data.payload.resume_id,
        vacancy_id=incoming_data.payload.vacancy_id,
        hh_response_id=incoming_data.id,
        session=session,
    ):
        return Response(status_code=status.HTTP_409_CONFLICT)

    # send in rabbit
    ...
    await HHController.save_matching(
        resume_id=incoming_data.payload.resume_id,
        vacancy_id=incoming_data.payload.vacancy_id,
        hh_response_id=incoming_data.id,
        session=session,
    )

    return Response(status_code=status.HTTP_200_OK)
