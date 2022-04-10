import time
from datetime import datetime
from typing import Optional


__all__ = ["convert_unixtime_to_datetime", "convert_unixtime"]


def convert_unixtime_to_datetime(value: int) -> str:
    return datetime.utcfromtimestamp(value).strftime("%Y-%m-%d %H:%M:%S")


def convert_unixtime(d: Optional[datetime] = None) -> int:
    value = d
    if d is None:
        value = datetime.now()
    return int(time.mktime(value.timetuple()))
