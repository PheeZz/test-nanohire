from utils.dependencies import async_session_maker
from .schemas import StrippedResumeResponse
from models import Response, ResponseStatus, Contact, ContactType, Vacancy
from uuid import uuid4, UUID
from sqlalchemy import select


async def add_vacancy_response_to_db(resume_response: dict, vacancy_id: str):
    """
    Добавляет отклик на вакансию в базу данных.

    Args:
        resume_response: Словарь с данными отклика
        vacancy_id: ID вакансии (строка UUID)

    Returns:
        UUID созданного Response
    """
    resp = StrippedResumeResponse.model_validate(resume_response)
    vacancy_uuid = UUID(vacancy_id)

    async with async_session_maker() as session:
        vacancy = await session.scalar(
            select(Vacancy).where(Vacancy.id == vacancy_uuid)
        )
        if not vacancy:
            raise ValueError(f"Vacancy with id={vacancy_id} not found")

        response_id = uuid4()

        new_response = Response(
            id=response_id,
            vacancy_id=vacancy_uuid,
            first_name=resp.first_name,
            middle_name=resp.middle_name,
            last_name=resp.last_name,
            hh_response_id=resp.id,
            status=ResponseStatus.NEW,
        )
        session.add(new_response)
        await session.flush()

        contacts_data = []
        for contact in resp.contacts:
            match contact.type:
                case "email":
                    type_ = ContactType.EMAIL
                case "phone":
                    type_ = ContactType.PHONE
                case "telegram":
                    type_ = ContactType.TELEGRAM
                case _:
                    type_ = ContactType.OTHER

            contacts_data.append(
                {
                    "id": uuid4(),
                    "response_id": response_id,
                    "type": type_,
                    "value": contact.value,
                }
            )

        if contacts_data:
            await session.run_sync(
                lambda sync_session: sync_session.bulk_insert_mappings(
                    Contact, contacts_data
                )
            )

        await session.commit()

        return response_id
