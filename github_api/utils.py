import logging
from datetime import timedelta

from .consts import PACKAGE_NAME
from .consts import WeekEnd

logging.basicConfig(
    format='%(asctime)s %(levelname)s %(message)s',
    level=logging.INFO)
log = logging.getLogger(PACKAGE_NAME)


_WEEKENDS = (WeekEnd.SATURDAY.value, WeekEnd.SUNDAY.value)


def is_weekend(dt):
    """
    >>> from datetime import datetime
    >>> is_weekend(datetime(2020, 3, 4).isoweekday())
    False
    >>> is_weekend(datetime(2020, 3, 7).isoweekday())
    True
    >>> is_weekend(datetime(2020, 3, 8).isoweekday())
    True
    """
    if dt in _WEEKENDS:
        return True
    return False


_ONE_WEEK = timedelta(days=7)
_DAY_SECONDS = (60 * 60 * 24)


def offset_weekdays(dt, start=True):
    """
    >>> from datetime import datetime
    >>> offset_weekdays(datetime(2020, 3, 7))
    172800
    >>> offset_weekdays(datetime(2020, 3, 8))
    86400
    """
    weekday = dt.isoweekday()
    if weekday == WeekEnd.SATURDAY.value:
        return 2 * _DAY_SECONDS if start else _DAY_SECONDS
    elif weekday == WeekEnd.SUNDAY.value:
        return _DAY_SECONDS if start else 2 * _DAY_SECONDS
    raise ValueError(f'{dt} is not Saturday or Sunday')


def calculate_days(start, end):
    """
    >>> from datetime import datetime
    >>> calculate_days(datetime(2020, 3, 4), datetime(2020, 3, 4)) # Wed-Wed
    0.0
    >>> calculate_days(datetime(2020, 3, 4), datetime(2020, 3, 5)) # Wed-Thr
    1.0
    >>> calculate_days(datetime(2020, 3, 4), datetime(2020, 3, 6)) # Wed-Fri
    2.0
    >>> calculate_days(datetime(2020, 3, 4), datetime(2020, 3, 7)) # Wed-Sat
    2.0
    >>> calculate_days(datetime(2020, 3, 4), datetime(2020, 3, 8)) # Wed-Sun
    2.0
    >>> calculate_days(datetime(2020, 3, 4), datetime(2020, 3, 9)) # Wed-Mon
    3.0
    >>> calculate_days(datetime(2020, 3, 7), datetime(2020, 3, 7)) # Sat-Sat
    0.0
    >>> calculate_days(datetime(2020, 3, 7), datetime(2020, 3, 8)) # Sat-Sun
    1.0
    >>> calculate_days(datetime(2020, 3, 7), datetime(2020, 3, 9)) # Sat-Mon
    0.0
    >>> calculate_days(datetime(2020, 3, 7), datetime(2020, 3, 9)) # Sun-Mon
    0.0
    >>> calculate_days(datetime(2020, 3, 4), datetime(2020, 3, 11)) # Wed-Wed
    5.0
    >>> calculate_days(datetime(2020, 3, 4), datetime(2020, 3, 18)) # Wed-Wed
    10.0
    >>> calculate_days(datetime(2020, 3, 4), datetime(2020, 3, 21)) # Wed-Sat
    12.0
    >>> calculate_days(datetime(2020, 3, 4, 9, 15, 0),
    ...                datetime(2020, 3, 4, 15, 15, 0))
    0.25
    >>> calculate_days(datetime(2020, 3, 4, 9, 15, 0),
    ...                datetime(2020, 3, 5, 15, 15, 0))
    1.25
    """
    elapsed = end - start
    if elapsed.days == 0:
        pass  # current day

    elif 1 < elapsed.days < 7:
        start_weekday = start.isoweekday()
        end_weekday = end.isoweekday()
        if is_weekend(start_weekday):
            offset = offset_weekdays(start)
            total = elapsed.total_seconds()
            if total < offset:
                return 0.0
            return (total - offset) / _DAY_SECONDS
        if is_weekend(end_weekday):
            offset = offset_weekdays(end, False)
            total = elapsed.total_seconds()
            if total < offset:
                return 0.0
            return (total - offset) / _DAY_SECONDS

        if start_weekday > end_weekday:
            delta = elapsed.total_seconds() - (2 * _DAY_SECONDS)
            return delta / _DAY_SECONDS  # include weekend

    elif 7 == elapsed.days:
        return 5.0

    elif 7 < elapsed.days:
        nextweek_date = start + _ONE_WEEK
        return 5.0 + calculate_days(nextweek_date, end)

    return elapsed.total_seconds() / _DAY_SECONDS
