from sqlalchemy.ext.asyncio import AsyncSession

from adapters.hh import HHAdapter, ResumeResponse
from adapters.hh.schemas import StrippedResumeResponse, StrippedContact
from exceptions.external import (
    HHApiTooManyRequestsError,
    HHApiUnauthorizedError,
    HHApiNotFoundError,
)
from exceptions.internal import InternalVacancyNotFoundError

from models import VacancyToResponseResume
from sqlalchemy import select
from aio_pika.patterns import RPC


class HHController:
    @staticmethod
    async def get_resume_data(resume_id: str) -> ResumeResponse | None:
        try:
            resume = await HHAdapter.get_resume_details(resume_id)
        except HHApiUnauthorizedError:
            # логирование, что авторизация не пройдена, возможно попытка обновить токен, если обновить не удалось
            # - отправка алерта в мессенджер/на почту
            return None
        except HHApiNotFoundError:
            # логирование, что резюме не найдено, возможно отправка алерта в мессенджер/на почту
            return None
        except HHApiTooManyRequestsError:
            # queue
            return None
        else:
            return resume

    @staticmethod
    async def is_matching_exist(
        resume_id: str,
        vacancy_id: str,
        hh_response_id: str,
        session: AsyncSession,
    ) -> bool:
        stmt = (
            select(VacancyToResponseResume)
            .where(
                VacancyToResponseResume.response_resume_id == resume_id,
                VacancyToResponseResume.vacancy_id == vacancy_id,
                VacancyToResponseResume.hh_response_id == hh_response_id,
            )
            .limit(1)
        )
        result = await session.execute(stmt)

        return result.scalar_one_or_none() is not None

    @staticmethod
    async def save_matching(
        resume_id: str,
        vacancy_id: str,
        hh_response_id: str,
        session: AsyncSession,
    ) -> None:
        matching = VacancyToResponseResume(
            response_resume_id=resume_id,
            vacancy_id=vacancy_id,
            hh_response_id=hh_response_id,
        )
        session.add(matching)
        await session.commit()

        return

    @classmethod
    async def send_vacancy_response(
        cls,
        rpc: RPC,
        resume_response: ResumeResponse,
        vacancy_id: str,
    ) -> None:
        stripped_contacts = [
            StrippedContact(
                type=contact.type.name,
                value=contact.contact_value,
            )
            for contact in resume_response.contact
        ]

        msg = StrippedResumeResponse(
            id=resume_response.id,
            first_name=resume_response.first_name,
            middle_name=resume_response.middle_name,
            last_name=resume_response.last_name,
            contacts=stripped_contacts,
        )
        try:
            await rpc.proxy.add_vacancy_response_to_db(
                resume_response=msg.model_dump(),
                vacancy_id=vacancy_id,
            )
        except ValueError:
            raise InternalVacancyNotFoundError
