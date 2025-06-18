from datetime import datetime
from zoneinfo import ZoneInfo


def utc_to_co(dt_utc: datetime) -> datetime:
    return dt_utc.astimezone(ZoneInfo("America/Bogota"))
