"""
Сервисный слой для работы с аутентификацией.
"""

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from models import User
from core.securiry import Security
from uuid import UUID
from fastapi import HTTPException, status


class AuthService:
    """Сервис для работы с аутентификацией"""

    @staticmethod
    async def register_user(
        email: str,
        password: str,
        first_name: str,
        last_name: str,
        middle_name: str | None,
        hh_manager_id: str,
        session: AsyncSession,
    ) -> User:
        """
        Регистрация нового пользователя.

        Args:
            email: Email пользователя
            password: Пароль (будет захэширован)
            first_name: Имя
            last_name: Фамилия
            middle_name: Отчество (опционально)
            hh_manager_id: ID менеджера в HeadHunter
            session: Сессия БД

        Returns:
            Созданный пользователь

        Raises:
            HTTPException 409: Если пользователь с таким email уже существует
        """
        # Проверяем, существует ли пользователь с таким email
        stmt = select(User).where(User.email == email.lower())
        result = await session.execute(stmt)
        existing_user = result.scalar_one_or_none()

        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="User with this email already exists",
            )

        hashed_password = Security.get_password_hash(password)

        new_user = User(
            email=email.lower(),
            password=hashed_password,
            first_name=first_name,
            last_name=last_name,
            middle_name=middle_name,
            hh_manager_id=hh_manager_id,
        )

        session.add(new_user)
        await session.commit()
        await session.refresh(new_user)

        return new_user

    @staticmethod
    async def authenticate_user(
        email: str,
        password: str,
        session: AsyncSession,
    ) -> User:
        """
        Аутентификация пользователя.

        Args:
            email: Email пользователя
            password: Пароль
            session: Сессия БД

        Returns:
            Аутентифицированный пользователь

        Raises:
            HTTPException 401: Если credentials неверные или пользователь неактивен
        """
        stmt = select(User).where(User.email == email.lower())
        result = await session.execute(stmt)
        user = result.scalar_one_or_none()

        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect email or password",
            )

        if not Security.verify_password(password, user.password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect email or password",
            )

        if not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User account is inactive",
            )

        return user

    @staticmethod
    async def get_user_by_id(user_id: UUID, session: AsyncSession) -> User:
        """
        Получить пользователя по ID.

        Args:
            user_id: ID пользователя
            session: Сессия БД

        Returns:
            Пользователь

        Raises:
            HTTPException 404: Если пользователь не найден
        """
        user = await session.get(User, user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found",
            )
        return user
