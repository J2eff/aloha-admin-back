import aioboto3
from settings import settings
from model import TABLE_NAME


__all__ = ["session", "db_setting", "get_table"]

session = aioboto3.Session()

db_setting = {
    "service_name": "dynamodb",
    "aws_access_key_id": settings.DATABASE_ACCESS_KEY,
    "aws_secret_access_key": settings.DATABASE_SECRET_KEY,
    "region_name": "ap-northeast-2",
    "endpoint_url": "https://dynamodb.ap-northeast-2.amazonaws.com",
}

if settings.PROJECT_ENV == "production":
    db_setting.update(
        {
            "endpoint_url": "https://dynamodb.ap-northeast-2.amazonaws.com",
        }
    )


async def get_table():
    async with session.resource(**db_setting) as client:
        table = await client.Table(TABLE_NAME)
        yield table
