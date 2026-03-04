from utils.dependencies import async_session_maker
from .schemas import StrippedResumeResponse
from models import Response, ResponseStatus, Contact, ContactType
from uuid import uuid4, UUID


async def add_vacancy_response_to_db(resume_response: dict, vacancy_id: UUID):
    """
    Добавляет отклик на вакансию в базу данных.

    Args:
        resume_response: Словарь с данными отклика
        vacancy_id: ID вакансии

    Returns:
        UUID созданного Response
    """
    resp = StrippedResumeResponse.model_validate(resume_response)

    async with async_session_maker() as session:
        # Генерируем ID для Response
        response_id = uuid4()

        # Создаем Response объект
        new_response = Response(
            id=response_id,
            vacancy_id=vacancy_id,
            first_name=resp.first_name,
            middle_name=resp.middle_name,
            last_name=resp.last_name,
            hh_response_id=resp.id,
            status=ResponseStatus.NEW,
        )
        session.add(new_response)

        # Подготавливаем данные для bulk insert Contacts
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
