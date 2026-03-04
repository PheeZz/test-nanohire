"""
Database models.
"""

from sqlalchemy import inspect

from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from uuid import uuid4, UUID
from sqlalchemy import (
    String,
    Text,
    DateTime,
    ForeignKey,
    Enum as SQLEnum,
    Index,
    Boolean,
)
from sqlalchemy.orm import validates
from sqlalchemy.orm.attributes import PASSIVE_NO_INITIALIZE
from datetime import datetime, timezone
from enum import Enum
import re


class Base(DeclarativeBase):
    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)


class User(Base):
    """Менеджер (пользователь)"""

    __tablename__ = "users"

    first_name: Mapped[str] = mapped_column(String(100), nullable=False)
    middle_name: Mapped[str] = mapped_column(String(100), nullable=True)
    last_name: Mapped[str] = mapped_column(String(100), nullable=False)
    email: Mapped[str] = mapped_column(
        String(255), unique=True, nullable=False, index=True
    )
    password: Mapped[str] = mapped_column(String(255), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )

    sensitive_data_updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )

    vacancies: Mapped[list["Vacancy"]] = relationship(
        "Vacancy", back_populates="manager", cascade="all, delete-orphan"
    )

    @validates("email")
    def validate_email(self, key: str, email: str) -> str:
        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            raise ValueError("Provided email is not valid")
        return email.lower()

    @validates("password", "is_active")
    def validate_sensitive_data(self, key: str, value):
        """Обновляет timestamp при изменении критичных полей для инвалидации JWT"""
        if self.id is not None:
            state = inspect(self)
            history = state.get_history(key, PASSIVE_NO_INITIALIZE)

            if history.has_changes():
                self.sensitive_data_updated_at = datetime.now(timezone.utc)

        return value


class Vacancy(Base):
    """Вакансия"""

    __tablename__ = "vacancies"

    title: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
        nullable=False,
    )

    # Relationships
    manager: Mapped["User"] = relationship("User", back_populates="vacancies")
    responses: Mapped[list["Response"]] = relationship(
        "Response", back_populates="vacancy", cascade="all, delete-orphan"
    )


class ResponseStatus(str, Enum):
    """Статусы отклика"""

    NEW = "new"
    VIEWED = "viewed"
    REJECTED = "rejected"


class ContactType(str, Enum):
    """Типы контактов"""

    EMAIL = "email"
    PHONE = "phone"
    TELEGRAM = "telegram"
    OTHER = "other"


class Response(Base):
    """Отклик на вакансию"""

    __tablename__ = "responses"

    vacancy_id: Mapped[UUID] = mapped_column(
        ForeignKey("vacancies.id", ondelete="CASCADE"), nullable=False
    )

    first_name: Mapped[str] = mapped_column(String(100), nullable=False)
    middle_name: Mapped[str | None] = mapped_column(String(100), nullable=True)
    last_name: Mapped[str] = mapped_column(String(100), nullable=False)

    hh_response_id: Mapped[str | None] = mapped_column(
        String(255), unique=True, nullable=True, index=True
    )

    status: Mapped[ResponseStatus] = mapped_column(
        SQLEnum(ResponseStatus, name="response_status"),
        default=ResponseStatus.NEW,
        nullable=False,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
        nullable=False,
    )

    vacancy: Mapped["Vacancy"] = relationship("Vacancy", back_populates="responses")
    contacts: Mapped[list["Contact"]] = relationship(
        "Contact", back_populates="response", cascade="all, delete-orphan"
    )

    __table_args__ = (
        Index("idx_response_vacancy_id", "vacancy_id"),
        Index("idx_response_status", "status"),
        Index("idx_response_vacancy_status", "vacancy_id", "status"),
    )


class Contact(Base):
    """Контактные данные кандидата"""

    __tablename__ = "contacts"

    response_id: Mapped[UUID] = mapped_column(
        ForeignKey("responses.id", ondelete="CASCADE"), nullable=False
    )
    type: Mapped[ContactType] = mapped_column(
        SQLEnum(ContactType, name="contact_type"), nullable=False
    )
    value: Mapped[str] = mapped_column(String(255), nullable=False)

    response: Mapped["Response"] = relationship("Response", back_populates="contacts")

    __table_args__ = (Index("idx_contact_response_id", "response_id"),)
