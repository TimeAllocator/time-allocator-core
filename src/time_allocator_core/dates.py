from datetime import datetime, timezone
from typing import Literal
from zoneinfo import ZoneInfo

Zone = Literal[
    "UTC",
    "America/New_York",
    "America/Chicago",
    "America/Denver",
    "America/Los_Angeles",
]


def to_utc(value: datetime) -> datetime:
    """Convert a datetime to UTC (always offset-aware)."""
    if value.tzinfo is None:
        return value.replace(tzinfo=timezone.utc)
    else:
        return value.astimezone(timezone.utc)


def now_utc() -> datetime:
    return datetime.now(timezone.utc)


def dt(
    year: int,
    month: int,
    day: int,
    hour: int = 0,
    minute: int = 0,
    second: int = 0,
    zone: Zone = "UTC",
) -> datetime:
    return datetime(
        year=year,
        month=month,
        day=day,
        hour=hour,
        minute=minute,
        second=second,
        tzinfo=ZoneInfo(zone),
    )
