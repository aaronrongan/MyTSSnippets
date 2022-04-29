# 创建一个欧洲股市数据库
# https://towardsdatascience.com/backtesting-trading-strategies-using-custom-data-in-zipline-e6fd65eeaca0

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from yahoofinancials import YahooFinancials

def download_csv_data(ticker, start_date, end_date, freq, path):
    
    yahoo_financials = YahooFinancials(ticker)

    df = yahoo_financials.get_historical_price_data(start_date, end_date, freq)

    df = pd.DataFrame(df[ticker]['prices']).drop(['date'], axis=1).rename(columns={'formatted_date':'date'}).loc[:, ['date','open','high','low','close','volume']].set_index('date')

    df.index = pd.to_datetime(df.index)

    df['dividend'] = 0

    df['split'] = 1

    # save data to csv for later ingestion
    df.to_csv(path, header=True, index=True)
    # plot the time series
    df.close.plot(title='{} prices --- {}:{}'.format(ticker, start_date, end_date));

# download_csv_data(ticker='ABN.AS', start_date='2017-01-01', end_date='2017-12-31', freq='daily', path='european/daily/abn.csv')
# download_csv_data(ticker='ABN.AS', start_date='2017-01-01', end_date='2017-12-31', freq='daily', path='abn.csv')

download_csv_data(ticker='^AEX', 
                  start_date='2017-01-01', 
                  end_date='2017-12-31', 
                  freq='daily', 
                  path='aex.csv')