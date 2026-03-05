from pydantic_settings import BaseSettings


class DatabaseConfig(BaseSettings):
    DB_HOST: str = "localhost"
    DB_PORT: int = 5432
    DB_NAME: str = "nanohire_hh_integration_test_db"
    DB_USER: str = "pheezz"
    DB_PASSWORD: str = "postgres"

    @property
    def db_url(self) -> str:
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    @property
    def SQLALCHEMY_DATABASE_URI(self) -> str:
        """Alias для db_url для совместимости"""
        return self.db_url

    class Config:
        env_file = ".env"


class RabbitMQConfig(BaseSettings):
    RABBITMQ_HOST: str = "localhost"
    RABBITMQ_PORT: int = 5672
    RABBITMQ_USER: str = "guest"
    RABBITMQ_PASSWORD: str = "guest"
    EXCHANGE_NAME: str = "nanohire_exchange"

    class Config:
        env_file = ".env"


class Config(DatabaseConfig, RabbitMQConfig):
    SERVICE_KEY: str = (
        "bebebeBababa"  # Сервисный ключ для аутентификации между сервисами
    )
    WEB_SERVER_PORT: int = 8080
    HH_API_TOKEN: str = "pipiPupu"
    HH_API_URL: str = "http://localhost:8080/api/v1/mock/hh"

    class Config:
        env_file = ".env"
