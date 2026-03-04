from pydantic import BaseModel


class ContactType(BaseModel):
    id: str
    name: str


class Contact(BaseModel):
    comment: str | None
    contact_value: str
    kind: str
    need_verification: bool | None
    preferred: bool
    type: ContactType
    verified: bool | None
    links: dict[str, str] | None


class ResumeResponse(BaseModel):
    id: str
    first_name: str
    last_name: str
    position: str
    contact: list[Contact]


class StrippedContact(BaseModel):
    value: str
    type: str


class StrippedResumeResponse(BaseModel):
    id: str
    first_name: str
    middle_name: str | None
    last_name: str
    contacts: list[StrippedContact]
