from typing import Any, AsyncGenerator, Annotated

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine, AsyncSession
from fastapi import Depends, HTTPException
from fastapi.security import APIKeyHeader, HTTPAuthorizationCredentials
from fastapi import Request
from core import settings

ENGINE = create_async_engine(settings.SQLALCHEMY_DATABASE_URI)
async_session_maker = async_sessionmaker(ENGINE, expire_on_commit=False)

security = APIKeyHeader(name="X-API-KEY", auto_error=True)


async def get_db_session() -> AsyncGenerator[AsyncSession, Any]:
    """Dependency для получения сессии БД"""
    try:
        async with async_session_maker() as session:
            yield session
    except SQLAlchemyError:
        await session.rollback()
        raise
    finally:
        await session.close()


async def verify_service_key(
    credentials: Annotated[HTTPAuthorizationCredentials, Depends(security)],
) -> None:
    """
    Dependency для проверки наличия и валидности service key.

    Извлекает service key из заголовка Authorization и сравнивает его
    с ожидаемым значением из настроек.

    Args:
        credentials: токен из заголовка X-API-KEY

    Raises:
        HTTPException 401: Если service key невалидный или отсутствует
    """

    service_key = credentials.credentials

    if service_key != settings.SERVICE_KEY:
        raise HTTPException(status_code=401, detail="Invalid service key")


def get_rpc(request: Request):
    rpc = request.app.state.rpc
    return rpc
