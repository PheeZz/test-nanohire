from .base import BaseCustomException


class InternalVacancyNotFoundError(BaseCustomException):
    def __init__(self, message: str = "Vacancy not found in the internal database."):
        self.message = message
        super().__init__(self.message)
