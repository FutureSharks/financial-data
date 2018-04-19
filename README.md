# financial-data

Intraday financial data files for backtesting or analysis. Currently this includes minute bars for:

- S&P 500 from 2010-2018 in USD (SPXUSD)
- NIKKEI 225 from 2010-2018 in JPY (JPXJPY)
- DAX 30 from 2010-2018 in EUR (GRXEUR)
- EUROSTOXX 50 from 2010-2018 in EUR (ETXEUR)

## Data file path structure

`data/<type>/<provider>/<instrument>`

For example, `data/stocks/histdata/sp500/DAT_ASCII_SPXUSD_M1_2010.csv` is stock data for the S&P 500 index from the histdata provider.

## Create a Pandas dataframe

```python
import pandas as pd

year = 2017
instrument = 'SPXUSD'
provider = 'histdata'
filename = 'data/stocks/{2}/{0}/DAT_ASCII_{0}_M1_{1}.csv'.format(instrument, year, provider)

price_data = pd.read_csv(filename, index_col=0, delimiter=';', header=None)

price_data.index.name = 'date'
price_data.index = pd.to_datetime(price_data.index)
price_data.drop(columns=[5], inplace=True)
columns={1: 'open', 2: 'high', 3: 'low', 4: 'close'}
price_data.rename(columns=columns, inplace=True)

price_data.head(3)
```

```
                        open     high     low    close
date
2017-01-02 18:00:00  2241.00  2244.50  2241.0  2243.50
2017-01-02 18:01:00  2243.75  2243.75  2243.0  2243.00
2017-01-02 18:02:00  2243.25  2243.25  2243.0  2243.25
```
