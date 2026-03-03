from typing import Any, AsyncGenerator, Annotated

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine, AsyncSession
from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from core import settings
from core.securiry import Security
from models import User

ENGINE = create_async_engine(settings.SQLALCHEMY_DATABASE_URI)
async_session_maker = async_sessionmaker(ENGINE, expire_on_commit=False)

security = HTTPBearer()


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


async def get_current_user(
    credentials: Annotated[HTTPAuthorizationCredentials, Depends(security)],
    session: Annotated[AsyncSession, Depends(get_db_session)],
) -> User:
    """
    Dependency для получения текущего аутентифицированного пользователя.

    Извлекает access токен из заголовка Authorization, валидирует его
    и возвращает объект пользователя.

    Args:
        credentials: Bearer токен из заголовка Authorization
        session: Сессия БД

    Returns:
        Аутентифицированный пользователь

    Raises:
        HTTPException 401: Если токен невалидный или отсутствует
    """

    token = credentials.credentials

    user = await Security.validate_token_and_get_user(
        token=token,
        token_type="access",
        session=session,
    )

    return user


async def verify_service_key(
    credentials: Annotated[HTTPAuthorizationCredentials, Depends(security)],
) -> None:
    """
    Dependency для проверки наличия и валидности service key.

    Извлекает service key из заголовка Authorization и сравнивает его
    с ожидаемым значением из настроек.

    Args:
        credentials: Bearer токен из заголовка Authorization

    Raises:
        HTTPException 401: Если service key невалидный или отсутствует
    """

    service_key = credentials.credentials

    if service_key != settings.SERVICE_KEY:
        raise HTTPException(status_code=401, detail="Invalid service key")
