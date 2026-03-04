from pydantic import BaseModel


class HHNewResponseOrInvitationVacancyWH(BaseModel):
    class NewResponseOrInvitationVacancyPayload(BaseModel):
        chat_id: str
        employer_id: str
        negotiation_date: str
        resume_id: str
        topic_id: str
        vacancy_id: str

    action_type: str
    id: str
    payload: NewResponseOrInvitationVacancyPayload
    subscription_id: str
    user_id: str
