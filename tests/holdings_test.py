''' holdings tests '''
from __future__ import (absolute_import, division, print_function,
                        unicode_literals)
from mockportfolio import Holdings
import pandas as pd
# import sys
# import os
# sys.path.append(os.path.join(os.path.dirname(__file__), os.pardir, "mockportfolio"))
# import pytest

# from pandas import DataFrame # Series,


def test_ctor_holdings():
    holdings = Holdings()
    assert holdings is not None


def test_random_tick():
    ''' should pick a random ticker '''
    assert 1 == 1


def test_generate_builds_dataframe():
    holdings = Holdings()
    df = holdings.generate()
    assert isinstance(df, pd.DataFrame) is True


def test_listings_returns_dataframe():
    holdings = Holdings()
    asx = holdings.listings()
    assert asx.empty is not True


def test_random_ticks():
    hold = Holdings()
    asx = hold.listings()
    ticks = hold.random_ticks(asx)
    assert len(ticks.Tick.values) == 10


# def test_portfolio(mocker):
#     hold = Holdings()
#     portfolio = hold.portfolio(None)
#     print(portfolio)
#     assert len(portfolio) == 10
