# financial-data
Intraday financial data files for backtesting or analysis. Currently this includes minute bars for:

- S&P 500 from 2010-2018 in USD (SPXUSD)
- NIKKEI 225 from 2010-2018 in JPY (JPXJPY)
- DAX 30 from 2010-2018 in EUR (GRXEUR)
- EUROSTOXX 50 from 2010-2018 in EUR (ETXEUR)
- Currencies pairs: AUD_JPY, AUD_USD, EUR_USD, GBP_USD, USD_CAD
- Cryptocurrencies pairs: BTC_USD, BTC_EUR, ETH_EUR

This package will parse the CSV files and return them as a [Pandas DataFrame](https://pandas.pydata.org/pandas-docs/stable/generated/pandas.DataFrame.html).

## Project moved to GitLab

Due to volume of data in the project I have moved it to Gitlab: https://gitlab.com/user4725345/pyfinancialdata
