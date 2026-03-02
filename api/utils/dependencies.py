from typing import Any, AsyncGenerator

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine, AsyncSession
from api.core import settings

ENGINE = create_async_engine(settings.SQLALCHEMY_DATABASE_URI)
async_session_maker = async_sessionmaker(ENGINE, expire_on_commit=False)


async def get_db_session() -> AsyncGenerator[AsyncSession, Any]:
    try:
        async with async_session_maker() as session:
            yield session
    except SQLAlchemyError:
        await session.rollback()
        raise
    finally:
        await session.close()
