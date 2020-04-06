from datetime import datetime

import pytest

from github_api.utils import calculate_days
from github_api.utils import is_weekend
from github_api.utils import offset_weekdays
from github_api.utils import parse_datetime
from github_api.utils import between_datetime


@pytest.mark.parametrize('dt,expected', [
    (datetime(2020, 3, 4).isoweekday(), False),
    (datetime(2020, 3, 7).isoweekday(), True),
    (datetime(2020, 3, 8).isoweekday(), True),
])
def test_is_weekend(dt, expected):
    assert is_weekend(dt) == expected


@pytest.mark.parametrize('dt,expected', [
    (datetime(2020, 3, 7), 172800),
    (datetime(2020, 3, 8), 86400),
])
def test_offset_weekdays(dt, expected):
    assert offset_weekdays(dt) == expected


@pytest.mark.parametrize('start,end,expected', [
    (datetime(2020, 3, 4), datetime(2020, 3, 4), 0.0),  # Wed-Wed
    (datetime(2020, 3, 4), datetime(2020, 3, 5), 1.0),  # Wed-Thr
    (datetime(2020, 3, 4), datetime(2020, 3, 6), 2.0),  # Wed-Fri
    (datetime(2020, 3, 4), datetime(2020, 3, 7), 2.0),  # Wed-Sat
    (datetime(2020, 3, 4), datetime(2020, 3, 8), 2.0),  # Wed-Sun
    (datetime(2020, 3, 4), datetime(2020, 3, 9), 3.0),  # Wed-Mon
    (datetime(2020, 3, 7), datetime(2020, 3, 7), 0.0),  # Sat-Sat
    (datetime(2020, 3, 7), datetime(2020, 3, 8), 1.0),  # Sat-Sun
    (datetime(2020, 3, 7), datetime(2020, 3, 9), 0.0),  # Sat-Mon
    (datetime(2020, 3, 7), datetime(2020, 3, 9), 0.0),  # Sun-Mon
    (datetime(2020, 3, 4), datetime(2020, 3, 11), 5.0),  # Wed-Wed
    (datetime(2020, 3, 4), datetime(2020, 3, 18), 10.0),  # Wed-Wed
    (datetime(2020, 3, 4), datetime(2020, 3, 21), 12.0),  # Wed-Sat
    (datetime(2020, 3, 4, 9, 15, 0), datetime(2020, 3, 4, 15, 15, 0), 0.25),
    (datetime(2020, 3, 4, 9, 15, 0), datetime(2020, 3, 5, 15, 15, 0), 1.25),
])
def test_calculate_days(start, end, expected):
    assert calculate_days(start, end) == expected


@pytest.mark.parametrize('s,format_,expected', [
    ('2020-04-06 08:50:30', None, datetime(2020, 4, 6, 8, 50, 30)),
    ('20200406', '%Y%m%d', datetime(2020, 4, 6, 0, 0, 0)),
])
def test_parse_datetime(s, format_, expected):
    if format_ is None:
        assert parse_datetime(s) == expected
    else:
        assert parse_datetime(s, format_) == expected


@pytest.mark.parametrize('dt,fromdate,todate,expected', [
    # normal
    (datetime(2020, 4, 6), datetime(2020, 4, 5), datetime(2020, 4, 7), True),
    (datetime(2020, 4, 6), None, datetime(2020, 4, 7), True),
    (datetime(2020, 4, 6), datetime(2020, 4, 5), None, True),
    (datetime(2020, 4, 6), None, None, True),
    # error
    (datetime(2020, 4, 4), datetime(2020, 4, 5), datetime(2020, 4, 7), False),
    (datetime(2020, 4, 4), datetime(2020, 4, 5), None, False),
    (datetime(2020, 4, 8), datetime(2020, 4, 5), datetime(2020, 4, 7), False),
    (datetime(2020, 4, 8), None, datetime(2020, 4, 7), False),
])
def test_between_datetime(dt, fromdate, todate, expected):
    assert between_datetime(dt, fromdate, todate) == expected
