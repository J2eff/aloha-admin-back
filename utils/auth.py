from typing import Optional
from fastapi.exceptions import HTTPException

from model import *
from utils.code import *
from querysets import *


__all__ = ["get_current_user"]


async def get_current_user(table, user_id: Optional[str], is_admin: bool = False) -> User:
    if user_id is None:
        raise HTTPException(**AUTH_REQUIRED)

    user = await query_user(table, user_id)
    if user is None:
        raise HTTPException(**AUTH_REQUIRED)

    if is_admin and not user.is_admin:
        raise HTTPException(**ONLY_ADMIN)

    return user
