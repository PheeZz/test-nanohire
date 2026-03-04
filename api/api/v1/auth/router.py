from fastapi import APIRouter, Body, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Annotated

from .schemas import (
    AuthUserS,
    RegisterUserS,
    AuthResponseS,
    TokenPairS,
    UserResponseS,
)
from .controller import AuthService
from utils.dependencies import get_db_session
from core.securiry import Security

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post(
    "/register",
    responses={
        status.HTTP_201_CREATED: {
            "description": "Пользователь успешно зарегистрирован, возвращает данные пользователя и пару токенов",
            "model": AuthResponseS,
        },
        status.HTTP_409_CONFLICT: {
            "description": "Ошибка регистрации, например, email уже используется",
            "content": {
                "application/json": {
                    "example": {"detail": "User with this email already exists"},
                }
            },
        },
    },
    summary="Регистрация нового пользователя",
    description="Создает нового пользователя и возвращает пару токенов (access + refresh)",
)
async def register(
    user_data: RegisterUserS,
    session: Annotated[AsyncSession, Depends(get_db_session)],
) -> AuthResponseS:
    # Регистрируем пользователя
    user = await AuthService.register_user(
        email=user_data.email,
        password=user_data.password,
        first_name=user_data.first_name,
        last_name=user_data.last_name,
        middle_name=user_data.middle_name,
        session=session,
    )

    # Создаем пару токенов
    token_pair = Security.create_token_pair(
        subject=str(user.id),
        sensitive_data_updated_at=user.sensitive_data_updated_at,
    )

    return AuthResponseS(
        user=UserResponseS.model_validate(user),
        tokens=TokenPairS(
            access_token=token_pair.access,
            refresh_token=token_pair.refresh,
        ),
    )


@router.post(
    "/login",
    responses={
        status.HTTP_200_OK: {
            "description": "Пользователь успешно аутентифицирован, возвращает данные пользователя и пару токенов",
            "model": AuthResponseS,
        },
        status.HTTP_401_UNAUTHORIZED: {
            "description": "Неверный email или пароль, или аккаунт неактивен",
            "content": {
                "application/json": {
                    "example": {"detail": "Incorrect email or password"},
                }
            },
        },
    },
    summary="Вход в систему",
    description="Аутентификация пользователя и получение пары токенов",
)
async def login(
    user_data: AuthUserS,
    session: Annotated[AsyncSession, Depends(get_db_session)],
) -> AuthResponseS:
    # noinspection PyTypeChecker
    user = await AuthService.authenticate_user(
        email=user_data.email,
        password=user_data.password,
        session=session,
    )

    token_pair = Security.create_token_pair(
        subject=str(user.id),
        sensitive_data_updated_at=user.sensitive_data_updated_at,
    )

    return AuthResponseS(
        user=UserResponseS.model_validate(user),
        tokens=TokenPairS(
            access_token=token_pair.access,
            refresh_token=token_pair.refresh,
        ),
    )


@router.post(
    "/refresh",
    status_code=status.HTTP_200_OK,
    summary="Обновление токенов",
    description="Получение новой пары токенов по refresh токену",
    responses={
        status.HTTP_200_OK: {
            "description": "Новая пара токенов успешно получена",
            "model": TokenPairS,
        },
        status.HTTP_401_UNAUTHORIZED: {
            "description": "Невалидный или просроченный refresh токен",
            "content": {
                "application/json": {
                    "example": {"detail": "Invalid refresh token"},
                }
            },
        },
    },
)
async def refresh_token_pair(
    refresh_token: Annotated[str, Body(..., embed=True)],
    session: Annotated[AsyncSession, Depends(get_db_session)],
) -> TokenPairS:

    user = await Security.validate_token_and_get_user(
        token=refresh_token,
        token_type="refresh",
        session=session,
    )

    token_pair = Security.create_token_pair(
        subject=str(user.id),
        sensitive_data_updated_at=user.sensitive_data_updated_at,
    )

    return TokenPairS(
        access_token=token_pair.access,
        refresh_token=token_pair.refresh,
    )
