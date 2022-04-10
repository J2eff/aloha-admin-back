from uuid import UUID
from typing import Optional, List
from pydantic import BaseModel, Field, EmailStr, constr, validator
from pydantic.fields import ModelField

from settings import settings
from .friend import FriendStatus

__all__ = [
    "SimpleUser",
    "User",
    "StrictUser",
    "UserRequest",
    "UserPagination",
    "UserReport",
    "UserReportRequest",
]

class SimpleUser(BaseModel):
    id: UUID = Field(title="일련번호")
    nickname: Optional[str] = Field(
        None,
        title="이름",
    )
    image: Optional[str] = Field(
        title="이미지",
        description="첫번째 이미지가 저장됩니다.",
    )
    def __init__(self, images: Optional[List[str]] = None, **kwargs):
        image = None
        if "image" in kwargs:
            image = kwargs.pop("image")

        if isinstance(images, list) and len(images) > 0:
            base_url = f"https://{settings.S3_BUCKET}.s3.ap-northeast-2.amazonaws.com/"
            if images[0].startswith(base_url):
                image = images[0]
            else:
                image = f"{base_url}{images[0]}"
        super().__init__(image=image, **kwargs)


class User(BaseModel):
    id: UUID = Field(title="일련번호")
    nickname: Optional[str] = Field(
        None,
        title="이름",
    )
    email: Optional[EmailStr] = Field(
        None,
        title="이메일",
        description="소셜 플랫폼에 따라 이메일이 없을 수도 있습니다.",
    )
    phone: Optional[str] = Field(
        None,
        title="휴대폰 번호",
        description="- 없이 표시",
    )
    images: List[str] = Field(
        title="이미지 목록",
        default_factory=list,
    )
    leisures: List[str] = Field(
        title="관심레저 목록",
        default_factory=list,
    )
    age: Optional[str] = Field(title="나이")
    gender: Optional[str] = Field(title="성별")
    corona: Optional[bool] = Field(title="코로나 접종")
    car: Optional[bool] = Field(title="차량 유무")
    region: Optional[dict] = Field(title="지역")

    mbti: Optional[str] = Field(title="MBTI")
    me: Optional[List[str]] = Field(title="나는?", default_factory=list)
    leisure1: Optional[str] = Field(title="레저 인터뷰 1")
    leisure2: Optional[str] = Field(title="레저 인터뷰 2")
    leisure3: Optional[str] = Field(title="레저 인터뷰 3")
    leisure4: Optional[str] = Field(title="레저 인터뷰 4")

    introduction: Optional[str] = Field(title="자기소개")

    friend_count: int = Field(title="친구 수", default=0)
    schedule_count: int = Field(title="일정 수", default=0)

    friend_status: Optional[FriendStatus] = Field(title="친구 상태")
    is_block: bool = Field(title="차단 여부", default=False)

    has_notification: bool = Field(title="안 읽음 알림 유무", default=False)

    is_admin: bool = Field(title="관리자 여부", default=False)

    def __init__(self, images: Optional[List] = None, **kwargs):
        base_url = f"https://{settings.S3_BUCKET}.s3.ap-northeast-2.amazonaws.com/"
        if images is None:
            images = []
        new_images = [
            f"{base_url}{image}" if not image.startswith(base_url) else image
            for image in images
        ]
        super().__init__(images=new_images, **kwargs)


class StrictUser(BaseModel):
    class Config:
        validate_assignment = True

    @validator("*", pre=True)
    def not_none(cls, v, field: ModelField):
        if not v:
            if field.default is None:
                return field.type_()
            return field.default
        else:
            return v
    id: UUID = Field(title="일련번호")
    nickname: Optional[str] = Field(
        default="Not Configured",
        title="이름",
    )
    email: Optional[EmailStr] = Field(
        default="default@default.dev",
        title="이메일",
        description="소셜 플랫폼에 따라 이메일이 없을 수도 있습니다.",
    )
    phone: Optional[str] = Field(
        default="Not Configured",
        title="휴대폰 번호",
        description="- 없이 표시",
    )
    images: List[str] = Field(
        title="이미지 목록",
        default_factory=list,
    )
    leisures: List[str] = Field(
        title="관심레저 목록",
        default_factory=list,
    )
    age: Optional[str] = Field(default="Not Configured", title="나이")
    gender: Optional[str] = Field(default="Not Configured",title="성별")
    corona: Optional[bool] = Field(default=False, title="코로나 접종")
    car: Optional[bool] = Field(default=False, title="차량 유무")
    region: Optional[dict] = Field(default={"region1": "Not Configured", "region2": "Not Configured"}, title="지역")

    mbti: Optional[str] = Field(default="Not Configured", title="MBTI")
    me: Optional[List[str]] = Field(default=list(), title="나는?")
    leisure1: Optional[str] = Field(default="Not Configured", title="레저 인터뷰 1")
    leisure2: Optional[str] = Field(default="Not Configured", title="레저 인터뷰 2")
    leisure3: Optional[str] = Field(default="Not Configured", title="레저 인터뷰 3")
    leisure4: Optional[str] = Field(default="Not Configured", title="레저 인터뷰 4")

    introduction: Optional[str] = Field(default="Not Configured", title="자기소개")

    friend_count: int = Field(title="친구 수", default=0)
    friend_status: Optional[str] = Field(default="Not Configured", title="친구 상태")
    is_block: bool = Field(title="차단 여부", default=False)

    has_notification: bool = Field(title="안 읽음 알림 유무", default=False)

    is_admin: bool = Field(title="관리자 여부", default=False)

    def __init__(self, images: Optional[List] = None, **kwargs):
        base_url = f"https://{settings.S3_BUCKET}.s3.ap-northeast-2.amazonaws.com/"
        if images is None:
            images = []
        new_images = [
            f"{base_url}{image}" if not image.startswith(base_url) else image
            for image in images
        ]
        super().__init__(images=new_images, **kwargs)


class UserRequest(BaseModel):
    nickname: Optional[str] = Field(
        title="이름",
    )
    phone: Optional[constr(strip_whitespace=True)] = Field(
        title="휴대전화",
        description="- 없이 입력해주세요",
    )
    leisures: Optional[list] = Field(title="관심레저 목록")
    age: Optional[str] = Field(title="나이")
    gender: Optional[str] = Field(title="성별")
    corona: Optional[bool] = Field(title="코로나 접종")
    car: Optional[bool] = Field(title="차량 유무")
    region: Optional[dict] = Field(title="지역")

    mbti: Optional[str] = Field(title="MBTI")
    me: Optional[List[str]] = Field(title="나는?", default_factory=list)
    leisure1: Optional[str] = Field(title="레저 인터뷰 1")
    leisure2: Optional[str] = Field(title="레저 인터뷰 2")
    leisure3: Optional[str] = Field(title="레저 인터뷰 3")
    leisure4: Optional[str] = Field(title="레저 인터뷰 4")

    introduction: Optional[str] = Field(title="자기소개")
    images: Optional[List[str]] = Field(title="이미지 목록")

    is_admin: Optional[bool] = Field(title="관리자 여부")


class UserPagination(BaseModel):
    data: List[User]
    next_cursor: Optional[str]


class UserReportRequest(BaseModel):
    content: str


class UserReport(BaseModel):
    id: UUID = Field(title="일련번호")
    content: str = Field(title="내용")
