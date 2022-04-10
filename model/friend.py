from enum import Enum
from pydantic import BaseModel, Field


__all__ = ["FriendStatus", "FriendRequest", "FriendResponse"]


class FriendStatus(str, Enum):
    REQUEST = "request"
    RECEIVED = "received"
    ACCEPT = "accept"
    REJECT = "reject"


class FriendRequest(BaseModel):
    user_id: str = Field(title="사용자 일련번호")


class FriendResponse(BaseModel):
    user_id: str = Field(title="사용자 일련번호")
    status: FriendStatus = Field(title="친구 상태")
