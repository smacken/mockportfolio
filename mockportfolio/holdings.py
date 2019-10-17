'''holdings generator'''
import pandas as pd


class Holdings(object):
    ''' trading holdings generator '''
    def __init__(self):
        pass

    def generate(self):
        ''' generate holdings history frame '''
        return pd.DataFrame()

    def listings(self):
        ''' get a dataframe of all listed tickers '''
        df = pd.read_csv('data/ASXListedCompanies.csv', skiprows=[0, 1])
        df.rename(
            columns={
                'Company name': 'Name',
                'ASX code': 'Tick',
                'GICS industry group': 'Industry'
            }, inplace=True)
        return df

    def random_ticks(self, listings, tick_count=10):
        ''' get a list of random tickers from the listings '''
        df = listings.sample(n=tick_count)
        return df

    def portfolio(self):
        pass
