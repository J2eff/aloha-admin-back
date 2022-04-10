import asyncio
from datetime import datetime, timedelta
from typing import Dict, Optional, Any, List, Tuple
from boto3.dynamodb.conditions import Key
from utils.date import convert_unixtime, convert_unixtime_to_datetime
from .user import query_user
from model import *

__all__ = [
    "query_schedule_item",
    "query_schedule_items_by_date",
    "query_schedule_items_by_user",
]

async def get_schedule_users(table, schedule: Dict[str, Any]) -> List[Dict[str, Any]]:
    schedule_users = schedule.get("users", [])
    query = []
    for user_id in schedule_users:
        query.append(query_user(table, user_id))

    users = await asyncio.gather(*query)
    new_users = []
    for user in users:
        if user is None:
            continue

        new_users.append(user.dict())

    return new_users

async def query_schedule_item(
    table, schedule_id: str, user_id: Optional[str] = None
) -> Optional[Schedule]:
    schedules = await table.query(
        KeyConditionExpression=Key(PK).eq(SCHEDULE_KEY.format(schedule_id=schedule_id))
        & Key(SK).eq(SCHEDULE),
    )
    if schedules["Count"] == 0:
        return None

    schedule = schedules["Items"][0]
    schedule["id"] = schedule_id
    schedule["users"] = await get_schedule_users(table, schedule)

    if user_id is not None:
        requests = await table.query(
            KeyConditionExpression=Key(PK).eq(
                SCHEDULE_KEY.format(schedule_id=schedule_id)
            )
            & Key(SK).eq(REQUEST_KEY.format(user_id=user_id)),
        )

        if requests["Count"] > 0:
            schedule["status"] = ScheduleStatus.REQUEST.value
        elif (
            user_id in [str(user["id"]) for user in schedule["users"]]
            and user_id != schedule["owner_id"]
        ):
            schedule["status"] = ScheduleStatus.ACCEPTED.value

    return Schedule(**schedule)
async def convert_schedule(table, schedules: List[Dict[str, Any]]) -> List[Schedule]:
    result = []
    for schedule in schedules:
        schedule["id"] = schedule[PK].split("#")[-1]
        schedule["users"] = await get_schedule_users(table, schedule)

        result.append(Schedule(**schedule))
    return result

async def query_schedule_items_by_date(table, date: Optional[int] = None):
    if date is None:
        now = datetime.now()
        now = now.replace(hour=0, minute=0, second=0, microsecond=0)
        now = now - timedelta(minutes=1)
        start = convert_unixtime(now)

        schedules = await table.query(
            IndexName=GSI_INDEX,
            KeyConditionExpression=Key(SK).eq(SCHEDULE) & Key(DK).begins_with(USER),
            FilterExpression="#start >= :start",
            ExpressionAttributeNames={"#start": "start"},
            ExpressionAttributeValues={":start": start},
        )
    else:
        standard_date = convert_unixtime_to_datetime(date).split(" ")[0]
        schedules = await table.query(
            IndexName=GSI_INDEX,
            KeyConditionExpression=Key(SK).eq(SCHEDULE) & Key(DK).begins_with(USER),
            FilterExpression="#start <= :date AND #end >= :date",
            ExpressionAttributeNames={"#start": "start_date", "#end": "end_date"},
            ExpressionAttributeValues={":date": standard_date},
        )

    return await convert_schedule(table, schedules["Items"])

async def query_schedule_items_by_user(table, user_id: str) -> int:
    schedules = await table.query(
        KeyConditionExpression=Key(PK).eq(USER_KEY.format(user_id=user_id))
        & Key(SK).begins_with(SCHEDULE),
    )
    schedule_ids = [item[SK].split("#")[-1] for item in schedules["Items"]]
    results = []
    for schedule_id in schedule_ids:
        schedule = await query_schedule_item(table, schedule_id)
        if schedule is not None:
            results.append(schedule)

    return len(results)