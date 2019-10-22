''' generator for transactions '''
import pandas as pd
from .holdings import Holdings
from .prices import Prices


class Transactions(object):
    ''' transaction generator '''
    def __init__(self, data_path='data/'):
        ''' ctor '''
        self.data_path = data_path
        self.holdings = Holdings(self.data_path)
        self.prices = Prices(self.data_path)

    def generate(self, total=10000):
        ''' generate portfolio transactions '''
        holding_sheet = self.holdings.generate(total)
        price_data = self.prices.get_prices()
        holding = {}
        for month in holding_sheet.keys():
            ticks = holding_sheet[month]
            remainder = 0
            month_total = 0
            month_prices = price_data[price_data.Date == month]
            for tick in ticks:
                amnt = ticks[tick]
                prices = month_prices[month_prices.Tick == tick]
                # todo: no prices for day
                # todo: nan for close price
                if prices.empty:
                    continue
                tick_prices = prices.iloc[0]
                current = holding[tick] if tick in holding else 0
                holding[tick] = tick_prices.Close
                month_total += round(amnt * tick_prices.Close, 2)
                diff = round(abs(current - holding[tick]), 3)
                print(tick, tick_prices.Close, current, diff)
                # if diff > 0:
                # add purchase transaction
                # elif diff < 0:
                # add sell transaction
            print(month, month_total, remainder)
        return pd.DataFrame()
