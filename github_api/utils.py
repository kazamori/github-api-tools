import logging
from datetime import datetime
from datetime import timedelta
from pathlib import Path

import pandas as pd


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


def parse_datetime(s, format_='%Y-%m-%d %H:%M:%S'):
    """
    >>> parse_datetime('2022-03-20 23:25:24')
    datetime.datetime(2022, 3, 20, 23, 25, 24)
    >>> parse_datetime(  #doctest: +NORMALIZE_WHITESPACE
    ...     '2022-03-20T23:25:24.000+09:00',
    ...     '%Y-%m-%dT%H:%M:%S.000%z')
    datetime.datetime(2022, 3, 20, 23, 25, 24,
    tzinfo=datetime.timezone(datetime.timedelta(seconds=32400)))
    """
    return datetime.strptime(s, format_)


def between_datetime(dt, fromdate, todate):
    """
    >>> from datetime import datetime
    >>> fromdate = datetime(2022, 3, 10)
    >>> todate = datetime(2022, 3, 20)
    >>> between_datetime(fromdate, fromdate, todate)
    True
    >>> between_datetime(todate, fromdate, todate)
    True
    >>> between_datetime(datetime(2022, 3, 12), fromdate, todate)
    True
    >>> between_datetime(datetime(2022, 3, 12), fromdate, None)
    True
    >>> between_datetime(datetime(2022, 3, 9), None, None)
    True
    >>> between_datetime(datetime(2022, 3, 9), None, todate)
    True
    >>> between_datetime(datetime(2022, 3, 9), fromdate, todate)
    False
    >>> between_datetime(datetime(2022, 3, 9), fromdate, None)
    False
    >>> between_datetime(datetime(2022, 3, 21), fromdate, todate)
    False
    >>> between_datetime(datetime(2022, 3, 21), None, todate)
    False
    """
    if fromdate is None:
        if todate is None:
            return True
        else:
            return dt <= todate

    if todate is None:
        return fromdate <= dt

    return fromdate <= dt <= todate


def is_before_date(dt, fromdate):
    """
    >>> from datetime import datetime
    >>> fromdate = datetime(2022, 3, 10)
    >>> is_before_date(datetime(2022, 3, 9), fromdate)
    True
    >>> is_before_date(datetime(2022, 3, 10), fromdate)
    False
    >>> is_before_date(datetime(2022, 3, 10), None)
    False
    """
    if fromdate is None:
        return False
    return dt < fromdate


def create_filename(owner_repo, api):
    """
    >>> from .consts import GithubAPI
    >>> owner_repo = 'kazamori/github-api-tools'
    >>> create_filename(owner_repo, GithubAPI.ACTIONS)
    'github-api-tools-actions.csv'
    >>> create_filename(owner_repo, GithubAPI.PULLS)
    'github-api-tools-pulls.csv'
    """
    repo_name = owner_repo.split('/')[-1]
    api_name = api.value
    return f'{repo_name}-{api_name}.csv'


def output_csv(args, data, filename):
    df = pd.DataFrame(data)
    df.to_csv(filename, index=False, columns=data.keys())
    path = Path(filename)
    log.info(f'wrote data into {path}')
    return path
