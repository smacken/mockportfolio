'''holdings generator'''
import pandas as pd
from .prices import Prices


class Holdings(object):
    ''' trading holdings generator '''
    def __init__(self, data_path='data/'):
        self.data_path = data_path

    def generate(self):
        ''' generate holdings history frame '''
        return pd.DataFrame()

    def listings(self):
        ''' get a dataframe of all listed tickers '''
        df = pd.read_csv(f'{self.data_path}ASXListedCompanies.csv', skiprows=[0, 1])
        df.rename(
            columns={
                'Company name': 'Name',
                'ASX code': 'Tick',
                'GICS industry group': 'Industry'
            }, inplace=True)
        return df

    def random_ticks(self, tickers, tick_count=10):
        ''' get a list of random tickers from the listings '''
        df = tickers.sample(n=tick_count)
        return df

    def portfolio(self, date_start, portfolio_size=10):
        ticks = self.random_ticks(self.listings())
        prices = Prices(self.data_path)
        tick_prices = prices.update(ticks.Tick.values)
        ticks = tick_prices.Tick.unique()
        if ticks < portfolio_size:
            pass

        price_pivot = tick_prices.pivot(index='Date', columns='Tick', values='Close')
        return price_pivot
