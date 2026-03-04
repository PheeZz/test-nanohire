"""
Database models.
"""

from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import String


class Base(DeclarativeBase):
    __abstract__ = True


class VacancyToResponseResume(Base):
    __tablename__ = "vacancy_to_response_resume"

    vacancy_id: Mapped[str] = mapped_column(String(255), primary_key=True)
    response_resume_id: Mapped[str] = mapped_column(String(255), primary_key=True)

    # насчет этого ID не до конца понял. Будет ли он одинаковый у нескольких одинаковых уведомлений
    hh_response_id: Mapped[str] = mapped_column(String(255), primary_key=True)
