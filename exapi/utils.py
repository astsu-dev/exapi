import datetime


def get_timestamp() -> int:
    """Returns current timestamp in milliseconds."""

    return int(datetime.datetime.now().timestamp() * 1000)


def get_iso_timestamp(timespec: str) -> str:
    """Returns current utc timestamp in iso format.

    Args:
        timespec: time specification for iso format.
    """

    return datetime.datetime.utcnow().isoformat(timespec=timespec)
