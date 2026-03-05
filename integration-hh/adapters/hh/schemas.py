from pydantic import BaseModel


class ContactType(BaseModel):
    id: str
    name: str


class Contact(BaseModel):
    comment: str | None = None
    contact_value: str
    kind: str
    need_verification: bool | None = None
    preferred: bool
    type: ContactType
    verified: bool | None = None
    links: dict[str, str] | None = None


class ResumeResponse(BaseModel):
    id: str
    first_name: str
    middle_name: str | None = None
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
