from enum import Enum
from uuid import UUID
from typing import List, Optional
from datetime import datetime, date
from pydantic import BaseModel, Field


from .user import SimpleUser


__all__ = ["Schedule", "ScheduleRequest", "ScheduleStatus", "ScheduleParticipate"]


class ScheduleStatus(str, Enum):
    REQUEST = "request"
    ACCEPTED = "accepted"


class Schedule(BaseModel):
    id: UUID = Field(title="일정 일련번호")
    owner_id: UUID = Field(title="일정 주인 일련번호")
    title: str = Field(title="제목")
    content: str = Field(title="내용")
    start: datetime
    end: datetime
    start_date: date
    end_date: date
    leisure_id: str = Field(title="레저 일련번호")
    skill: int = Field(title="실력")
    max_count: int
    location: dict = Field(title="장소")
    tags: list = Field(title="태그")
    users: List[SimpleUser] = Field(title="참가자", default_factory=list)
    status: Optional[ScheduleStatus] = Field(title="상태")
    chat_id: Optional[str] = Field(title="채팅방 일련번호", default=None)
    is_time_decided: bool = Field(title="시간 무관 체크 여부")


class ScheduleRequest(BaseModel):
    title: str = Field(title="제목")
    content: str = Field(title="내용")
    start: datetime
    end: datetime
    is_time_decided: bool = Field(title="시간 무관 체크 여부")
    leisure_id: str = Field(title="레저 일련번호")
    skill: int = Field(title="실력")
    max_count: int
    location: dict = Field(title="장소")
    tags: list = Field(title="태그")


class ScheduleParticipate(BaseModel):
    date: date
    is_me: bool = Field(default=False)
