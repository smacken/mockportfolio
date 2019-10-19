'''holdings generator'''
import pandas as pd
from pypfopt.efficient_frontier import EfficientFrontier
from pypfopt import risk_models
from pypfopt import expected_returns
from pypfopt.discrete_allocation import DiscreteAllocation, get_latest_prices
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

    def build_portfolio(self, price_pivot, portfolio_total=10000):
        ''' build a portfolio '''
        mu = expected_returns.mean_historical_return(price_pivot)
        shrink = risk_models.CovarianceShrinkage(price_pivot)
        S = shrink.ledoit_wolf()
        ef = EfficientFrontier(mu, S, weight_bounds=(0, 0.2), gamma=0.8)
        weights = ef.max_sharpe()
        latest_prices = get_latest_prices(price_pivot)

        da = DiscreteAllocation(weights, latest_prices, total_portfolio_value=portfolio_total)
        allocation, leftover = da.lp_portfolio()
        # print("Discrete allocation:", allocation)
        weights = {k: v for k, v in weights.items() if weights[k] > 0.0}
        return weights

    def portfolio(self, date_start, portfolio_size=10):
        ticks = self.random_ticks(self.listings())
        prices = Prices(self.data_path)
        tick_prices = prices.update(ticks.Tick.values)
        ticks = tick_prices.Tick.unique()
        if ticks < portfolio_size:
            pass

        price_pivot = tick_prices.pivot(index='Date', columns='Tick', values='Close')
        return price_pivot
