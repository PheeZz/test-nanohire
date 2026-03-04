from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from models import Vacancy, Response, ResponseStatus, User


class NotificationController:
    @classmethod
    async def list_mapping_manager_responses(
        cls, session: AsyncSession
    ) -> dict[str, dict[str, int | str]]:
        """
        Получить маппинг менеджера и количества новых откликов на его вакансии.

        Args:
            session: Сессия БД

        Returns:
            Словарь {manager_id: {"name": "Имя Фамилия", "count": количество_откликов}}
        """
        stmt = (
            select(
                Vacancy.manager_id,
                User.first_name,
                func.count(Response.id).label("response_count"),
            )
            .join(Response, Vacancy.id == Response.vacancy_id)
            .join(User, Vacancy.manager_id == User.id)
            .where(Response.status == ResponseStatus.NEW)
            .group_by(Vacancy.manager_id, User.first_name)
        )

        result = await session.execute(stmt)
        rows = result.all()

        return {
            str(row.manager_id): {
                "name": row.first_name,
                "count": row.response_count,
            }
            for row in rows
        }
