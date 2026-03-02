from datetime import datetime, timedelta, timezone
from typing import Any, Literal

import jwt
import bcrypt

from api.core import settings
from dataclasses import dataclass


@dataclass(frozen=True)
class JWTPair:
    access: str
    refresh: str


class Security:
    @classmethod
    def create_token_pair(
        cls,
        subject: str | Any,
        sensitive_data_updated_at: datetime,
    ) -> JWTPair:
        return JWTPair(
            access=cls._create_token(
                subject=subject,
                expires_delta=timedelta(
                    minutes=settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES
                ),
                sensitive_data_updated_at=sensitive_data_updated_at,
            ),
            refresh=cls._create_token(
                subject=subject,
                expires_delta=timedelta(days=settings.JWT_REFRESH_TOKEN_EXPIRE_DAYS),
                sensitive_data_updated_at=sensitive_data_updated_at,
            ),
        )

    @classmethod
    def _create_token(
        cls,
        subject: str | Any,
        expires_delta: timedelta,
        sensitive_data_updated_at: datetime,
        type_: Literal["access", "refresh"] = "access",
    ) -> str:
        expire = datetime.now(timezone.utc) + expires_delta
        to_encode = {
            "sub": str(subject),
            "sdu": sensitive_data_updated_at.timestamp(),
            "type": type_,
            "exp": expire,
            "iat": datetime.now(timezone.utc).timestamp(),
        }

        return jwt.encode(
            to_encode,
            settings.JWT_SECRET,
            algorithm=settings.JWT_ALGORITHM,
        )

    @classmethod
    def verify_token(
        cls, token: str, type_: Literal["access", "refresh"] = "access"
    ) -> dict[str, Any]:
        try:
            payload = jwt.decode(
                token,
                settings.JWT_SECRET,
                algorithms=[settings.JWT_ALGORITHM],
            )
            if payload.get("type") != type_:
                raise jwt.InvalidTokenError("Invalid token type")
            return payload
        except jwt.ExpiredSignatureError:
            raise jwt.ExpiredSignatureError("Token has expired")
        except jwt.InvalidTokenError as e:
            raise jwt.InvalidTokenError(f"Invalid token: {str(e)}")

    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        return bcrypt.checkpw(
            plain_password.encode(encoding="utf-8"),
            hashed_password.encode(encoding="utf-8"),
        )

    @staticmethod
    def get_password_hash(password: str) -> str:
        return bcrypt.hashpw(
            password.encode(encoding="utf-8"), bcrypt.gensalt()
        ).decode("utf-8")
