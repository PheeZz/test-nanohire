from pydantic_settings import BaseSettings


class ApiConfig(BaseSettings):
    """API configuration for notifications service."""

    API_BASE_URL: str = "http://localhost:8000"
    API_SERVICE_KEY: str = "bebebeBababa"

    class Config:
        env_file = ".env"


class SchedulerConfig(BaseSettings):
    SCHEDULER_TIMEZONE: str = "Europe/Moscow"
    SCHEDULER_HOUR: int = 8
    SCHEDULER_MINUTE: int = 0

    class Config:
        env_file = ".env"


class Config(ApiConfig, SchedulerConfig):
    NOTIFICATION_BATCH_SIZE: int = 10


settings = Config()
