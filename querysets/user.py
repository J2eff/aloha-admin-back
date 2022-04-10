import asyncio
from typing import Dict, Optional, Any, List, Tuple
from math import ceil
from boto3.dynamodb.conditions import Key, Attr

from model import *

__all__ = [
    "query_user",
    "put_user",
    "get_user_friend_count",
    "get_user_friend",
    "get_friend_status",
    "get_user_block",
    "put_user_block",
    "delete_user_block",
    "check_user_block",
    "get_user_block_id",
    "query_user_all"
]


def _get_update_query_response(user_data: Dict[str, Any]) -> Tuple[str, Dict[str, Any]]:
    update_expression = f'SET '
    attributes_value_dict = {}

    if nickname := user_data["nickname"]:
        update_expression += "nickname= :nickname, "
        attributes_value_dict[":nickname"] = nickname

    if email := user_data["email"]:
        update_expression += "email= :email, "
        attributes_value_dict[":email"] = email

    if phone := user_data["phone"]:
        update_expression += "phone= :phone, "
        attributes_value_dict[":phone"] = phone

    if images := user_data["images"]:
        update_expression += "images= :images, "
        attributes_value_dict[":images"] = images

    if leisures := user_data["leisures"]:
        update_expression += "leisures= :leisures, "
        attributes_value_dict[":leisures"] = leisures

    if age := user_data["age"]:
        update_expression += "age= :age, "
        attributes_value_dict[":age"] = age

    if gender := user_data["gender"]:
        update_expression += "gender= :gender, "
        attributes_value_dict[":gender"] = gender

    if corona := user_data["corona"]:
        update_expression += "corona= :corona, "
        attributes_value_dict[":corona"] = corona

    if car := user_data["car"]:
        update_expression += "car= :car, "
        attributes_value_dict[":car"] = car

    if region := user_data["region"]:
        update_expression += "#R= :region, "
        attributes_value_dict[":region"] = region

    if mbti := user_data["mbti"]:
        update_expression += "mbti = :mbti, "
        attributes_value_dict[":mbti"] = mbti

    if me := user_data["me"]:
        update_expression += "me= :me, "
        attributes_value_dict[":me"] = me

    if leisure1 := user_data["leisure1"]:
        update_expression += "leisure1= :leisure1, "
        attributes_value_dict[":leisure1"] = leisure1

    if leisure2 := user_data["leisure2"]:
        update_expression += "leisure2= :leisure2, "
        attributes_value_dict[":leisure2"] = leisure2

    if leisure3 := user_data["leisure3"]:
        update_expression += "leisure3= :leisure3, "
        attributes_value_dict[":leisure3"] = leisure3

    if leisure4 := user_data["leisure4"]:
        update_expression += "leisure4= :leisure4, "
        attributes_value_dict[":leisure4"] = leisure4

    if introduction := user_data["introduction"]:
        update_expression += "introduction= :introduction, "
        attributes_value_dict[":introduction"] = introduction

    if friend_count := user_data["friend_count"]:
        update_expression += "friend_count= :friend_count, "
        attributes_value_dict[":friend_count"] = friend_count

    if friend_status := user_data["friend_status"]:
        update_expression += "friend_status= :friend_status, "
        attributes_value_dict[":friend_status"] = friend_status

    if is_block := user_data["is_block"]:
        update_expression += "is_block= :is_block, "
        attributes_value_dict[":is_block"] = is_block

    if has_notification := user_data["has_notification"]:
        update_expression += "has_notification= :has_notification, "
        attributes_value_dict[":has_notification"] = has_notification

    if is_admin := user_data["is_admin"]:
        update_expression += "is_admin= :is_admin, "
        attributes_value_dict[":is_admin"] = is_admin

    update_expression = update_expression[0:len(update_expression) - 2]
    return update_expression, attributes_value_dict


async def query_user_all(table) -> List[SimpleUser]:
    filters = dict()
    filters[DK] = USER
    users = await table.scan(
        FilterExpression=Attr(DK).eq(USER)
    )

    users_list = []
    for user in users["Items"]:
        user["id"] = user[PK].split("#")[-1]
        users_list.append(SimpleUser(**user))



    return users_list


async def query_user(table, user_id: str) -> Optional[User]:
    """
    사용자 데이터 조회.
    사용자의 일련번호를 기반으로 프로필 데이터 조회.
    """
    users = await table.query(
        KeyConditionExpression=Key(PK).eq(USER_KEY.format(user_id=user_id))
        & Key(SK).eq(PROFILE),
    )

    if users["Count"] == 0:
        return None
    user = users["Items"][0]
    user["id"] = user_id

    return User(**user)

async def put_user(table, user_id: str, data: Dict[str, Any]) -> User:
    """
    사용자 데이터 저장.
    저장 시, 사용자의 휴대폰 번호, 닉네임 유무에 따라 관련 데이터도 같이 저장.
    """
    user = await query_user(table, user_id)
    user_data = {
        PK: USER_KEY.format(user_id=user_id),
        SK: PROFILE,
        DK: USER,
    }
    if user is not None:
        user_data.update(user.dict())
        del user_data["id"]

    user_data.update({k: v for k, v in data.items() if v is not None and k != "id"})

    query = []
    if user_data.get("phone"):
        if user.phone:
            query.append(
                table.delete_item(
                    Key={
                        PK : USER_KEY.format(user_id=user_id),
                        SK : PHONE_KEY.format(phone=user.phone)
                    }
                )
            )
        query.append(
            table.put_item(
                Item={
                    PK : USER_KEY.format(user_id=user_id),
                    SK : PHONE_KEY.format(phone=user_data["phone"]),
                    DK : PHONE
                }
            )
        )

    update_expression, expression_attributes_values = _get_update_query_response(user_data)

    if len(expression_attributes_values.keys()) > 0:
        if ":region" in expression_attributes_values.keys():
            query.append(
                table.update_item(
                    Key={
                        PK: USER_KEY.format(user_id=user_id),
                        SK: PROFILE,
                    },
                    UpdateExpression=update_expression,
                    ExpressionAttributeValues=expression_attributes_values,
                    ExpressionAttributeNames={
                        "#R": "region"
                    }
                )
            )
        else:
            query.append(
                table.update_item(
                    Key={
                        PK: USER_KEY.format(user_id=user_id),
                        SK: PROFILE,
                    },
                    UpdateExpression=update_expression,
                    ExpressionAttributeValues=expression_attributes_values,
                )
            )

    await asyncio.gather(*query)

    user_data["id"] = user_id
    return User(**user_data)


async def get_user_friend_count(table, user_id: str) -> int:
    friends = await table.query(
        KeyConditionExpression=Key(PK).eq(USER_KEY.format(user_id=user_id))
        & Key(SK).begins_with(FRIEND)
    )
    return len(
        list(
            filter(
                lambda f: f.get("status") == FriendStatus.ACCEPT.value, friends["Items"]
            )
        )
    )


async def get_user_friend(table, user_id: str) -> List[User]:
    friends = await table.query(
        KeyConditionExpression=Key(PK).eq(USER_KEY.format(user_id=user_id))
        & Key(SK).begins_with(FRIEND)
    )

    friend_ids = [
        user[SK].split("#")[-1]
        for user in friends["Items"]
        if user.get("status") == FriendStatus.ACCEPT.value
    ]
    results = []
    for user in friend_ids:
        user_data = await query_user(table, user)
        if user_data is not None:
            results.append(user_data)

    return results


async def get_friend_status(table, user_id: str, friend_id: str) -> Optional[str]:
    friend = await table.query(
        KeyConditionExpression=Key(PK).eq(
            USER_KEY.format(user_id=user_id),
        )
        & Key(SK).eq(
            FRIEND_KEY.format(user_id=friend_id),
        )
    )

    if friend["Count"] > 0:
        return friend["Items"][0]["status"]

    return None


async def get_user_block(table, user_id: str):
    blocks = await table.query(
        KeyConditionExpression=Key(PK).eq(USER_KEY.format(user_id=user_id))
        & Key(SK).begins_with(BLOCK)
    )
    results = []
    for block in blocks["Items"]:
        user_id = block[SK].split("#")[-1]
        user = await query_user(table, user_id)
        if user is not None:
            results.append(user)

    return results


async def get_user_block_id(table, user_id: str) -> List[str]:
    blocks = await table.query(
        KeyConditionExpression=Key(PK).eq(USER_KEY.format(user_id=user_id))
        & Key(SK).begins_with(BLOCK)
    )
    results = []
    for block in blocks["Items"]:
        user = block[SK].split("#")[-1]
        results.append(user)

    return results


async def put_user_block(
    table,
    user_id: str,
    target_id: str,
):
    await table.put_item(
        Item={
            PK: USER_KEY.format(user_id=user_id),
            SK: BLOCK_KEY.format(user_id=target_id),
        }
    )


async def delete_user_block(table, user_id: str, target_id: str):
    await table.delete_item(
        Key={
            PK: USER_KEY.format(user_id=user_id),
            SK: BLOCK_KEY.format(user_id=target_id),
        }
    )


async def check_user_block(table, user_id: str, target_id: str) -> bool:
    block = await table.query(
        KeyConditionExpression=Key(PK).eq(USER_KEY.format(user_id=user_id))
        & Key(SK).eq(BLOCK_KEY.format(user_id=target_id))
    )

    return block["Count"] > 0
