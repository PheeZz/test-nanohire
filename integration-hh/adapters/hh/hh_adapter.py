import aiohttp

from core import settings
from loguru import logger
from .schemas import ResumeResponse
from exceptions.external import (
    HHApiTooManyRequestsError,
    HHApiUnauthorizedError,
    HHApiNotFoundError,
)


class HHAdapter:
    API_URL = settings.HH_API_URL

    @classmethod
    async def get_resume_details(cls, resume_id: str) -> ResumeResponse | None:
        """
        Тут правильно наверное было бы добавить REDIS для кеширования резюме на N часов, чтобы
        лишний раз не триггерить HTTP 429. Если же все таки ловим - положить в отдельную очередь на повторную обработку.
        """
        url = f"{cls.API_URL}/resumes/{resume_id}"

        async with (
            aiohttp.ClientSession(
                headers={"Authorization": f"Bearer {settings.HH_API_TOKEN}"}
            ) as session,
            session.get(url) as response,
        ):
            if response.ok:
                return ResumeResponse.model_validate(
                    await response.json(encoding="utf-8")
                )

            else:
                match response.status:
                    case 403:
                        logger.warning(
                            "Авторизация не пройдена, проверьте токен"
                        )  # тут можно либо обновить токен, либо отправить алерт в мессенджер/на почту, если обновить не удалось
                        raise HHApiUnauthorizedError
                    case 404:
                        logger.warning(f"Резюме с id {resume_id} не найдено")
                        raise HHApiNotFoundError
                    case 429:
                        logger.warning(
                            "Превышен лимит запросов к API, попробуйте позже"
                        )  # тут можно положить в отдельную очередь на повторную обработку,
                        # дабы HH не долбил нас запросами пока мы в 429, а мы не потеряли данные
                        raise HHApiTooManyRequestsError

                    case _:
                        logger.warning(
                            f"Неизвестная ошибка при запросе резюме с id {resume_id}, статус код: {response.status}."
                            f" Ответ: {await response.text()}"
                        )

                return None
