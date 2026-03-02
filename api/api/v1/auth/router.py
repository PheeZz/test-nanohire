from fastapi import APIRouter
from .schemas import AuthUserS
from fastapi import Body, Depends
from typing import Annotated
from api.utils.dependencies import get_db_session

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register")
async def register(user_data: AuthUserS, session: Depends(get_db_session)): ...


@router.post("/login")
async def login(user_data: AuthUserS, session: Depends(get_db_session)): ...


@router.post("/refresh")
async def refresh_token_pair(
    refresh_token: Annotated[
        str,
        Body(
            ...,
            embed=True,
        ),
    ],
    session: Depends(get_db_session),
): ...
