''' prices tests '''
from __future__ import (absolute_import, division, print_function,
                        unicode_literals)
from datetime import datetime
from mockportfolio import Prices


def test_ctor_prices():
    p = Prices()
    assert p is not None


def test_prev_weekday():
    # sat should become friday
    day = '2019-10-19'
    start_datetime = datetime.strptime(day, "%Y-%m-%d")
    p = Prices()
    weekday = p.prev_weekday(start_datetime)
    assert weekday == datetime.strptime('2019-10-18', "%Y-%m-%d")


def test_prev_weekday_for_weekday():
    # sat should become friday
    day = '2019-10-18'
    start_datetime = datetime.strptime(day, "%Y-%m-%d")
    p = Prices()
    weekday = p.prev_weekday(start_datetime)
    assert weekday == datetime.strptime('2019-10-18', "%Y-%m-%d")


def test_next_weekday():
    # sat should become mon
    day = '2019-10-19'
    start_datetime = datetime.strptime(day, "%Y-%m-%d")
    p = Prices()
    weekday = p.next_weekday(start_datetime)
    assert weekday == datetime.strptime('2019-10-21', "%Y-%m-%d")


def test_next_weekday_for_weekday():
    # fri should become friday
    day = '2019-10-18'
    start_datetime = datetime.strptime(day, "%Y-%m-%d")
    p = Prices()
    weekday = p.next_weekday(start_datetime)
    assert weekday == datetime.strptime('2019-10-18', "%Y-%m-%d")


def test_monthlist():
    start = '2017-01-09'
    end = '2018-12-27'
    p = Prices()
    months = p.monthlist([start, end])
    assert len(months) == 24


def test_monthlist_nextweek():
    start = '2017-01-09'
    end = '2018-12-27'
    p = Prices()
    months = [p.next_weekday(x) for x in p.monthlist([start, end])]
    assert len(months) == 24


def test_update_for_tickers():
    tickers = ['TNE', 'DMP']
    p = Prices()
    price_data = p.update(tickers, '2019-01-14')
    assert len(price_data.Tick.values) > 0
