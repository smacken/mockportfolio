''' '''
from yahoo_historical import Fetcher
from datetime import datetime, timedelta
import pandas as pd


class Prices(object):
    ''' ticker price retrieval'''
    def __init__(self, data_path='data/'):
        self.data_path = data_path

    def to_date_list(self, date):
        ''' convert a date into a date array for price retrieval '''
        date_list = []
        date_list.extend([date.year, date.month, date.day])
        return date_list

    def prev_weekday(self, adate):
        ''' get the last trading day '''
        if adate.weekday() <= 4:
            return adate
        adate -= timedelta(days=1)
        while adate.weekday() > 4:  # Mon-Fri are 0-4
            adate -= timedelta(days=1)
        return adate

    def get_asx(self, tick, start_date, end_date):
        ''' get prices for date range '''
        tick_code = '%s.ax' % tick
        ticker = Fetcher(tick_code, start_date, end_date)
        time_series = ticker.getHistorical()
        time_series['Tick'] = tick
        time_series.rename(columns=lambda x: x.strip(), inplace=True)
        return time_series

    def update(self, tickers, start='2017-01-09'):
        ''' update prices for a given set of tickers '''
        price_pkl = f'{self.data_path}Prices.pkl'
        try:
            price_data = pd.read_pickle(price_pkl)
        except Exception:
            price_data = pd.DataFrame(data={'Tick': []})

        now = self.prev_weekday(datetime.now())
        now_date = self.to_date_list(datetime.now())
        for tick in tickers:
            existing = price_data[price_data['Tick'] == tick]
            tick_code = '%s.ax' % tick
            start_datetime = datetime.strptime(start, "%Y-%m-%d").strftime('%Y-%m-%d')
            start_date = self.to_date_list(start_datetime)
            print(tick_code, start_date, now_date)
            try:
                if existing.empty:
                    time_series = self.get_asx(tick, start_date, now_date)
                    if not time_series.empty:
                        print('new ', tick_code)
                        price_data = price_data.append(time_series, ignore_index=True)
                        continue

                # fill in gaps i.e. xxx-start->end-xx-now
                existing_min = datetime.strptime(existing.Date.min(), '%Y-%m-%d').date()
                existing_max = datetime.strptime(existing.Date.max(), '%Y-%m-%d').date()
                if start_datetime.date() < existing_min:
                    series = self.get_asx(tick, start_date, self.to_date_list(existing_min))
                    if not series.empty:
                        price_data = price_data.append(series, ignore_index=True)
                if now.date() > existing_max:
                    series = self.get_asx(tick, self.to_date_list(existing_max), now_date)
                    if not series.empty:
                        price_data = price_data.append(series, ignore_index=True)
            except Exception as ex:
                print('unable to get tick: ', tick_code, ex)
                continue
        price_data.drop_duplicates(['Tick', 'Date'], keep='first', inplace=True)
        price_data.to_pickle(price_pkl)
        return price_data
