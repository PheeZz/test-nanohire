from pydantic import BaseModel


class StrippedContact(BaseModel):
    value: str
    type: str


class StrippedResumeResponse(BaseModel):
    id: str
    first_name: str
    middle_name: str | None
    last_name: str
    contacts: list[StrippedContact]
