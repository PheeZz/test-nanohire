from adapters.hh import HHAdapter, ResumeResponse
from exceptions.external import (
    HHApiTooManyRequestsError,
    HHApiUnauthorizedError,
    HHApiNotFoundError,
)


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
