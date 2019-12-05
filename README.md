# financial-data

Intraday financial data files for backtesting or analysis. Currently this includes minute bars for:

- S&P 500 from 2010-2018 in USD (SPXUSD)
- NIKKEI 225 from 2010-2018 in JPY (JPXJPY)
- DAX 30 from 2010-2018 in EUR (GRXEUR)
- EUROSTOXX 50 from 2010-2018 in EUR (ETXEUR)
- Currencies pairs: AUD_JPY, AUD_USD, EUR_USD, GBP_USD, USD_CAD
- Cryptocurrencies pairs: BTC_USD, BTC_EUR, ETH_EUR

This package will parse the CSV files and return them as a [Pandas DataFrame](https://pandas.pydata.org/pandas-docs/stable/generated/pandas.DataFrame.html).

Pull requests welcome.

## Data file path structure

`data/<type>/<provider>/<instrument>`

For example, `data/stocks/histdata/sp500/DAT_ASCII_SPXUSD_M1_2010.csv` is stock data for the S&P 500 index from the histdata provider.

## Examples

#### BTC

```python
import pyfinancialdata
data = pyfinancialdata.get(provider='bitstamp', instrument='BTC_USD', year=2017)
data.tail(3)
                     open      high       low     close     price
date
2017-12-31 23:57:00  13908.73  13913.26  13874.99  13913.26  13913.26
2017-12-31 23:58:00  13913.26  13953.83  13884.69  13953.77  13953.77
2017-12-31 23:59:00  13913.28  13913.28  13867.18  13880.00  13880.00
```

#### S&P 500

```python
import pyfinancialdata
data = pyfinancialdata.get(provider='histdata', instrument='SPXUSD', year=2017)
data.tail(3)
                        open     high      low    close    price
date
2017-12-29 16:55:00  2668.75  2668.75  2668.00  2668.25  2668.25
2017-12-29 16:57:00  2667.75  2668.50  2667.75  2668.00  2668.00
2017-12-29 16:58:00  2668.25  2668.50  2667.75  2668.50  2668.50
```

#### EUR/USD

```python
import pyfinancialdata
data = pyfinancialdata.get(provider='oanda', instrument='EUR_USD', year=2017)
data.tail(3)
                       close     high      low     open  volume    price
date
2017-12-29 21:57:00  1.20045  1.20071  1.20004  1.20018      50  1.20045
2017-12-29 21:58:00  1.20041  1.20041  1.20041  1.20041       1  1.20041
2017-12-29 21:59:00  1.20039  1.20039  1.19970  1.20036      14  1.20039
```

### Optional time grouping for longer timeframes

For details see the [Pandas Grouper](https://pandas.pydata.org/pandas-docs/stable/generated/pandas.Grouper.html) documentation.

1 hour bars:

```python
import pyfinancialdata
data = pyfinancialdata.get(provider='oanda', instrument='EUR_USD', year=2017, time_group='60min')
data.tail(3)
                       close     high      low     open    price
date
2017-12-29 19:00:00  1.20093  1.20142  1.20072  1.20140  1.20093
2017-12-29 20:00:00  1.19982  1.20108  1.19976  1.20098  1.19982
2017-12-29 21:00:00  1.20039  1.20071  1.19922  1.19984  1.20039
```

Or 1 day bars for multiple years:

```python
import pyfinancialdata
data = pyfinancialdata.get_multi_year(provider='oanda', instrument='EUR_USD', years=[2014, 2015, 2016, 2017], time_group='1d')
data.head(3)
              close     high      low     open    price
date
2014-01-01  1.37642  1.37738  1.37424  1.37534  1.37642
2014-01-02  1.36653  1.37756  1.36296  1.37644  1.36653
2014-01-03  1.35888  1.36720  1.35825  1.36654  1.35888
```
