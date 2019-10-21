''' generator for transactions '''
import pandas as pd
from .holdings import Holdings


class Transactions(object):
    ''' transaction generator '''
    def __init__(self, data_path='data/'):
        ''' ctor '''
        self.holdings = Holdings(self.data_path)

    def generate(self, total=10000):
        ''' generate portfolio transactions '''
        holding_sheet = self.holdings.generate(total)
        for month in holding_sheet.keys():
            pass
        return pd.DataFrame()
