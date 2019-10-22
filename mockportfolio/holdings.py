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

    def generate(self, total=10000, start='2017-01-09', end='2018-12-27'):
        ''' generate holdings history frame '''
        p = Prices(self.data_path)
        portfolio = self.portfolio(start)
        holding_folio = {}
        months = [p.next_weekday(x).strftime('%Y-%m-%d') for x in p.monthlist([start, end])]
        months.append(end)
        for month in months:
            ''' rebalance portfolio /adjust holdings'''
            price_pivot = portfolio.loc[start:month]
            if len(price_pivot.index) < 10:
                continue
            allocation = self.build_portfolio(price_pivot, total)
            holding_folio[month] = allocation
        return holding_folio

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
        ''' build a portfolio from price data'''
        mu = expected_returns.mean_historical_return(price_pivot)
        shrink = risk_models.CovarianceShrinkage(price_pivot)
        S = shrink.ledoit_wolf()
        ef = EfficientFrontier(mu, S, weight_bounds=(0, 0.2), gamma=0.8)
        weights = ef.max_sharpe()
        weights = ef.clean_weights()
        latest_prices = get_latest_prices(price_pivot)
        weights = {k: v for k, v in weights.items() if weights[k] > 0.0}
        da = DiscreteAllocation(weights, latest_prices, total_portfolio_value=portfolio_total)
        allocation, leftover = da.lp_portfolio()
        # print("Discrete allocation:", allocation)
        return allocation

    def portfolio(self, date_start, portfolio_size=10):
        ''' build a random portfolio of prices, presented in pivot '''
        ticks = self.random_ticks(self.listings())
        prices = Prices(self.data_path)
        tick_prices = prices.update(ticks.Tick.values, date_start)
        tick_prices = tick_prices[tick_prices.Tick.isin(ticks.Tick.values.tolist())]
        tickers = tick_prices.Tick.unique()
        if len(tickers) < portfolio_size:
            # add additional random ticks
            remaining = portfolio_size - len(tickers)
            additional = self.random_ticks(self.listings(), remaining)
            add_prices = prices.update(additional.Tick.values, date_start)
            add_prices = add_prices[add_prices.Tick.isin(additional.Tick.values.tolist())]
            tick_prices = pd.concat([tick_prices, add_prices])
            pass

        price_pivot = tick_prices.pivot(index='Date', columns='Tick', values='Close')
        return price_pivot
