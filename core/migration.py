import boto3

from model.database import DK, PK, SK

from .database import db_setting
from model import TABLE_NAME, GSI_INDEX

__all__ = ["Migration"]

schemas = {
    "TableName": TABLE_NAME,
    "KeySchema": [
        {"AttributeName": PK, "KeyType": "RANGE"},
        {"AttributeName": SK, "KeyType": "RANGE"},
    ],
    "AttributeDefinitions": [
        {"AttributeName": PK, "AttributeType": "S"},
        {"AttributeName": SK, "AttributeType": "S"},
        {"AttributeName": DK, "AttributeType": "S"},
    ],
    "GlobalSecondaryIndexes": [
        {
            "IndexName": GSI_INDEX,
            "KeySchema": [
                {"AttributeName": SK, "KeyType": "RANGE"},
                {"AttributeName": DK, "KeyType": "RANGE"},
            ],
            "Projection": {"ProjectionType": "ALL"},
            "ProvisionedThroughput": {
                "ReadCapacityUnits": 5,
                "WriteCapacityUnits": 5,
            },
        },
    ],
    "ProvisionedThroughput": {
        "ReadCapacityUnits": 5,
        "WriteCapacityUnits": 5,
    },
}

update = {
    "TableName": TABLE_NAME,
    "AttributeDefinitions": [
        {"AttributeName": PK, "AttributeType": "S"},
        {"AttributeName": SK, "AttributeType": "S"},
        {"AttributeName": DK, "AttributeType": "S"},
    ],
    "KeySchema": [
        {"AttributeName": PK, "KeyType": "RANGE"},
        {"AttributeName": SK, "KeyType": "RANGE"},
    ],
}

class Migration:
    def __init__(self, **kwargs):
        self.client = None
        self.resource = None

    def get_client(self):
        self.client = boto3.client(**db_setting)

    def get_resource(self):
        self.resource = boto3.resource(**db_setting)

    def get_tables(self):
        return self.client.list_tables()["TableNames"]

    def migrate(self):
        self.get_client()
        self.get_resource()
        tables = self.get_tables()

        if not TABLE_NAME in tables:
            t = self.resource.create_table(**schemas)
            t.meta.client.get_waiter("table_exists").wait(TableName=TABLE_NAME)


    def reset(self):
        self.get_client()
        self.get_resource()

        tables = self.get_tables()
        if TABLE_NAME in tables:
            t = self.resource.Table(TABLE_NAME)
            t.delete()
