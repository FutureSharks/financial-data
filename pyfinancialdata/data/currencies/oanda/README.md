# Oanda

https://www.oanda.com/


Example showing how to download prices:

```python
from pyfinancialdata import oanda_prices

instruments = ['AUD_USD', 'AUD_JPY', 'EUR_USD', 'GBP_USD', 'USD_CAD']

for instrument in instruments:
    for year in range(2005, 2019):
        for month in range(1, 13):
            print('Getting {0}-{1} {2}'.format(month, year, instrument))
            oanda_prices.get_oanda_prices(
                csv_file='pyfinancialdata/data/currencies/oanda/{0}/{1}/oanda-{0}-{1}-{2}.csv'.format(
                    instrument,
                    year,
                    month
                ),
                instrument=instrument,
                year=year,
                month=month
            )
```
