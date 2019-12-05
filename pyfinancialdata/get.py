# -*- coding: utf-8 -*-

import pandas as pd
import os
import glob


basepath = os.path.dirname(__file__)
data_dir = os.path.abspath(os.path.join(basepath, 'data'))


def get(provider, instrument, year, price_calculation='close', time_group=None, drop_non_price_columns=False):
    '''
    Select the provider as each one has different CSV file structure
    '''
    if provider == 'oanda':
        price_data = pd.DataFrame()
        csv_files = glob.glob('{0}/currencies/oanda/{1}/{2}/*.csv'.format(data_dir, instrument, year))
        for csv_file in csv_files:
            price_data = price_data.append(pd.read_csv(csv_file, index_col=0))

    elif provider == 'kraken':
        filename = '{0}/cryptocurrencies/kraken/{1}/{2}.csv'.format(data_dir, instrument, year)
        price_data = pd.read_csv(filename, index_col=0)

    elif provider == 'bitstamp':
        filename = '{0}/cryptocurrencies/bitstamp/{1}/{2}.csv'.format(data_dir, instrument, year)
        price_data = pd.read_csv(filename, index_col=0)

    elif provider == 'histdata':
        filename = '{0}/stocks/histdata/{1}/DAT_ASCII_{1}_M1_{2}.csv'.format(data_dir, instrument, year)
        price_data = pd.read_csv(filename, index_col=0, delimiter=';', header=None)
        price_data.drop(columns=[5], inplace=True)
        columns={1: 'open', 2: 'high', 3: 'low', 4: 'close'}
        price_data.rename(columns=columns, inplace=True)

    else:
        raise Exception('Unkown provider {0}'.format(provider))

    '''
    Set the index and sort out the index
    '''
    price_data.index.name = 'date'
    price_data.index = pd.to_datetime(price_data.index)
    # Sort by index
    price_data.sort_index(inplace=True)
    # Remove duplicate index rows
    price_data = price_data[~price_data.index.duplicated(keep='first')]

    '''
    Optional timegrouping for larger timeframes
    '''
    if time_group:
        grouped_data = pd.DataFrame({
            'close': price_data.groupby(pd.Grouper(freq=time_group)).close.last(),
            'high': price_data.groupby(pd.Grouper(freq=time_group)).high.max(),
            'low': price_data.groupby(pd.Grouper(freq=time_group)).low.min(),
            'open': price_data.groupby(pd.Grouper(freq=time_group)).open.first(),
        })
        price_data = grouped_data

    '''
    Calculate a price column if required
    '''
    if price_calculation:
        if price_calculation == '4by4':
            price_data['price'] = (price_data['open'] + price_data['high'] + price_data['low'] + price_data['close']) / 4
        elif price_calculation == 'open':
            price_data['price'] = price_data['open']
        elif price_calculation == 'close':
            price_data['price'] = price_data['close']
        price_data = price_data.dropna(subset=['price'])


    '''
    Drop all columns except for price if required
    '''
    if drop_non_price_columns:
        for col in list(price_data.columns):
            if col != 'price':
                del price_data[col]

    return price_data


def get_multi_year(years, instrument, provider='oanda', price_calculation='close', time_group=None, drop_non_price_columns=False):
    '''
    This will get and concatenate multiple years into one dataframe
    '''
    year_dfs = []

    for year in years:
        year_dfs.append(
            get(
                instrument=instrument,
                provider=provider,
                year=year,
                price_calculation=price_calculation,
                time_group=time_group,
                drop_non_price_columns=drop_non_price_columns,
            )
        )

    # Concatenate the dataframes
    price_data = pd.concat(year_dfs)
    # Sort by index
    price_data.sort_index(inplace=True)
    # Deduplicate just in case
    price_data = price_data[~price_data.index.duplicated(keep='first')]
    # Remove any missing data
    price_data.dropna(axis=0, inplace=True)

    return price_data
