
#获取股票在某段时间内的股价，并用Matplotlib或pyecharts/seaborn显示，
#以后还会加上技术指标数据的显示

import tushare as ts
import pandas as pd
# import os
import matplotlib.pyplot as plt
import seaborn as sns
import seaborn.linearmodels as snsl
from datetime import datetime
import tushare as ts


#作者：CiferZ
#链接：https://www.jianshu.com/p/bf9c20ef160e

# import pandas.DataFrame as pdf
import csv

token='f20927201ecc20e3cea9279abacfbb1d39a9624820d9b2f94613f722'
# ts.set_token(token)
pro=ts.pro_api(token)
sns.set()

startdate='2013-1-5'
enddate = datetime.today() #开始时间结束时间，选取最近一年的数据

#start = datetime(end.year-1,end.month,end.day)
enddate = str(enddate)[0:10]
#start = str(start)[0:10]

#这里是未复权数据
#stock = ts.get_hist_data('300388',startdate,enddate)#选取一支股票
#这里是前复权数据
# stock = pro.daily(ts_code='000001.SZ', start_date='20180701', end_date='20180718')

stock = ts.pro_bar(ts_code='300327.SZ', api=None, adj='qfq', start_date=startdate, end_date=enddate)
print(type(stock))
# stock = ts.pro_bar(ts_code='300388.SZ', api=None, start_date=startdate, end_date=enddate, freq='D', asset='E',adj = 'qfq', ma = [], factors = None,adjfactor = False, contract_type = '', retry_count = 3)
stockline = [datetime.strptime(d, '%Y%m%d').date() for d in stock.trade_date]
mean60=stock.close.rolling(window=60).mean()
plt.figure(figsize=(12, 6))
plt.plot(stockline,stock.close, '-', label = stock.ts_code[0])
plt.plot(stockline,mean60 , '-', label = stock.ts_code[0])
# stock = stock.sort_index(ascending=True)
# stock.close['20150101':].plot()
# stock.close.plot()
# stock.close.rolling(60).mean().plot();

# stock['close'].plot(legend=True ,figsize=(10,4))
plt.show()



