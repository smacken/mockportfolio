''' holdings tests '''
from __future__ import (absolute_import, division, print_function,
                        unicode_literals)
from mockportfolio import Holdings
import pandas as pd
# import mockportfolio
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), os.pardir, "mockportfolio"))
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
