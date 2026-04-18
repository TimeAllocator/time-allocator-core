from datetime import datetime, timezone


def to_utc(dt: datetime) -> datetime:
    """Convert a datetime to UTC (always offset-aware)."""
    if dt.tzinfo is None:
        return dt.replace(tzinfo=timezone.utc)
    else:
        return dt.astimezone(timezone.utc)


def now_utc() -> datetime:
    return datetime.now(timezone.utc)
