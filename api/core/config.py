from pydantic_settings import BaseSettings


class JWTConfig(BaseSettings):
    JWT_SECRET: str = "your_secret_key"
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7


class DatabaseConfig(BaseSettings):
    DB_HOST: str = "localhost"
    DB_PORT: int = 5432
    DB_NAME: str = "nanohire_test_db"
    DB_USER: str = "postgres"
    DB_PASSWORD: str = "postgres"

    @property
    def db_url(self) -> str:
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"


class RabbitMQConfig(BaseSettings):
    RABBITMQ_HOST: str = "localhost"
    RABBITMQ_PORT: int = 5672
    RABBITMQ_USER: str = "guest"
    RABBITMQ_PASSWORD: str = "guest"
    EXCHANGE_NAME: str = "nanohire_exchange"


class Config(JWTConfig, DatabaseConfig, RabbitMQConfig): ...
