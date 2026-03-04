class BaseCustomException(Exception):
    """Base class for custom exceptions."""

    pass


class HHApiTooManyRequestsError(BaseCustomException):
    def __init__(self, message: str = "Too many requests to HH API."):
        self.message = message
        super().__init__(self.message)


class HHApiUnauthorizedError(BaseCustomException):
    def __init__(self, message: str = "Unauthorized access to HH API."):
        self.message = message
        super().__init__(self.message)


class HHApiNotFoundError(BaseCustomException):
    def __init__(self, message: str = "Resource not found in HH API."):
        self.message = message
        super().__init__(self.message)
