import asyncio
from fastapi import APIRouter, Depends, HTTPException
from typing import List
import logging

from model import *
from utils.code import *
from querysets import *
from utils import JWTBearer, get_current_user
from core import get_table
logger = logging.getLogger(__name__)


__all__ = ["router"]

router = APIRouter(prefix="/users", tags=["user"])

@router.get( "/")
async def get_all_user(
        table=Depends(get_table),
):

    user_list = await query_user_all(table)


    return user_list


@router.get(
    "/{user_id}/",
    response_model=User,
    summary="사용자 조회",
    description="""사용자 조회 API
---
사용자 ID 기반으로 해당 유저의 데이터를 조회합니다.
""",
)
async def get_user(
    user_id: str,
    table=Depends(get_table),
):
    [user, friend_status, friend_count, is_block, schedule_count] = await asyncio.gather(
        *[
            query_user(table, user_id),
            get_friend_status(table, user_id, user_id),
            get_user_friend_count(table, user_id),
            check_user_block(table, user_id, user_id),
            query_schedule_items_by_user(table,user_id)
        ]
    )

    if user is None:
        raise HTTPException(**NOT_FOUND)

    user.friend_status = friend_status
    user.friend_count = friend_count
    user.is_block = is_block
    user.schedule_count= schedule_count

    return user


@router.patch(
    "/{user_id}/",
    response_model=User,
    summary="사용자 수정",
    description="""사용자 수정 API
---
""",
)
async def update_user(
    user_id: str,
    data: UserRequest,
    current_user_id: str = Depends(JWTBearer()),
    table=Depends(get_table),
):
    current_user = await get_current_user(table, current_user_id)


    user = await query_user(table, user_id)
    if user is None:
        raise HTTPException(**NOT_FOUND)

    user = current_user.dict()
    user.update(data.dict())
    return await put_user(table, current_user_id, user)

