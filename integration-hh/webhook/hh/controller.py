from sqlalchemy.ext.asyncio import AsyncSession

from adapters.hh import HHAdapter, ResumeResponse
from exceptions.external import (
    HHApiTooManyRequestsError,
    HHApiUnauthorizedError,
    HHApiNotFoundError,
)

from models import VacancyToResponseResume
from sqlalchemy import select


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
