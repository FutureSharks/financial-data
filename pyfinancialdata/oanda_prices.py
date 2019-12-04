# -*- coding: utf-8 -*-

import os
import time
import v20
import calendar
import datetime
import pandas as pd


class OandaAccount(object):
    '''
    A wrapper for working with Oanda
    '''
    def __init__(self,
            oanda_access_token,
            hostname='api-fxpractice.oanda.com',
            datetime_format='UNIX'
        ):
        self.oanda_access_token = oanda_access_token
        self.hostname = hostname
        self.datetime_format = datetime_format
        self.api = v20.Context(hostname=self.hostname, token=self.oanda_access_token, datetime_format=datetime_format)

    def _return_as_dict(self, item):
        return self._un_stringify(item.dict())

    def _un_stringify(self, data):
        result = data
        if isinstance(data, list):
            return list(map(self._un_stringify, data))
        if isinstance(data, str):
            s = data
            if s.isdigit():
                return int(s)
            try:
                s = float(s)
            except ValueError:
                pass
            return s
        if isinstance(data, dict):
            result = data.copy()
            for key, val in result.items():
                result[key] = self._un_stringify(val)
        return result

    def get_candles(self, instrument, from_time=None, to_time=None, granularity='M1'):
        '''
        Gets historical prices for an instrument
        '''
        response = self.api.instrument.candles(instrument=instrument, fromTime=from_time, toTime=to_time, granularity=granularity)
        if response.status != 200:
            raise Exception('ERROR: {0}'.format(response.body['errorMessage']))
        candles = response.get('candles')
        return [self._return_as_dict(item) for item in candles]

    def get_candles_by_count(self, instrument, count=500, granularity='M1'):
        '''
        Gets historical prices for an instrument by count
        '''
        response = self.api.instrument.candles(instrument=instrument, count=count, granularity=granularity)
        if response.status != 200:
            raise Exception('ERROR: {0}'.format(response.body['errorMessage']))
        candles = response.get('candles')
        return [self._return_as_dict(item) for item in candles]


def create_candles_df(prices):
    '''
    Creates a Pandas DataFrame from a list of Oanda candles
    '''
    fixed_price_data = []

    for candle in prices:
        candle.update(candle['mid'])
        candle.pop('mid', None)
        candle.pop('complete', None)
        candle['open'] = candle.pop('o')
        candle['high'] = candle.pop('h')
        candle['low'] = candle.pop('l')
        candle['close'] = candle.pop('c')
        fixed_price_data.append(candle)

    price_data = pd.DataFrame(fixed_price_data)
    price_data['time'] = pd.to_datetime(price_data['time'], unit='s')
    price_data.set_index('time', inplace=True)

    # Deduplicate
    price_data.sort_index(inplace=True)
    price_data = price_data[~price_data.index.duplicated(keep='first')]

    return price_data


def get_oanda_prices(csv_file, instrument, year, month, granularity='M1', return_df=False):
    '''
    Gets a month of historical candle prices from the Oanda API and saves them as CSV files

    Example:

    from pybacktester import get_oanda_prices
    get_oanda_prices(csv_file='GBP_USD-2014-05.csv', instrument='GBP_USD', year=2014, month=5)
    '''
    # Account for getting candles
    oanda_account = OandaAccount(os.environ['oanda_access_token'])

    # Calculate UNIX times for start/end of month
    month_range = calendar.monthrange(year, month)
    month_start = datetime.datetime(year, month, 1, 0, 0, 0, 0, datetime.timezone(offset=datetime.timedelta(0))).timestamp()
    # If we are getting data for the current month then the month_end must be set to current time
    if month == datetime.date.today().month and year == datetime.date.today().year:
        month_end = time.time()
    else:
        month_end = datetime.datetime(year, month, month_range[1], 23, 59, 0, 0, datetime.timezone(offset=datetime.timedelta(0))).timestamp()
    oanda_count_limit = 4800
    oanda_count_window = oanda_count_limit * 60

    window_start = month_start
    window_end = window_start + oanda_count_window

    # Get the candle data
    month_candles = []
    while True:
        candles = oanda_account.get_candles(instrument=instrument, from_time=window_start, to_time=window_end, granularity=granularity)
        month_candles.extend(candles)
        if window_end == month_end:
            break
        window_end = min(month_end, window_end + oanda_count_window)
        window_start = window_end - oanda_count_window

    print('Downloaded {0} prices for {1}-{2}'.format(len(month_candles), year, month))

    if len(month_candles) == 0:
        return

    # Create a Pandas DataFrame
    price_data = create_candles_df(month_candles)

    if return_df:
        return price_data
    else:
        # Save to CSV file
        price_data.to_csv(csv_file)
