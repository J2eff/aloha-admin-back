from core import session, db_setting, Migration
from model import *
import boto3
import asyncio
import sys


async def init_data(is_reset):
    db_client = boto3.client(**db_setting)
    table = db_client.list_tables()["TableNames"]

    if TABLE_NAME not in table:
        db = Migration()
        db.migrate()
    elif is_reset:
        db = Migration()
        db.reset()
        db.migrate()


if __name__ == "__main__":
    is_reset = "--reset" in sys.argv
    asyncio.run(init_data(is_reset))
