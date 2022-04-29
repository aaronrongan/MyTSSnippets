
#获取股票在某段时间内的股价，并用Matplotlib或pyecharts/seaborn显示，
#以后还会加上技术指标数据的显示

import tushare as ts
import pandas as pd
# import os
import matplotlib.pyplot as plt
import seaborn as sns
import seaborn.linearmodels as snsl
from datetime import datetime
import talib 


token='f20927201ecc20e3cea9279abacfbb1d39a9624820d9b2f94613f722'

pro=ts.pro_api(token)
sns.set()

startdate='2013-1-5'
enddate = datetime.today() #开始时间结束时间，选取最近一年的数据


enddate = str(enddate)[0:10]
#start = str(start)[0:10]

#这里是未复权数据
#stock = ts.get_hist_data('300388',startdate,enddate)#选取一支股票
#这里是前复权数据
# stock = pro.daily(ts_code='000001.SZ', start_date='20180701', end_date='20180718')

stock = ts.pro_bar(ts_code='300383.SZ', api=None, adj='qfq', start_date=startdate, end_date=enddate)
print(type(stock))

closed=stock['close'].values
    #获取均线的数据，通过timeperiod参数来分别获取 5,10,20 日均线的数据。
ma5=talib.SMA(closed,timeperiod=5)
ma10=talib.SMA(closed,timeperiod=10)
ma20=talib.SMA(closed,timeperiod=20)

    #打印出来每一个数据
print (closed)
print (ma5)
print (ma10)
print (ma20)

    #通过plog函数可以很方便的绘制出每一条均线
plt.plot(closed)
plt.plot(ma5)
plt.plot(ma10)
plt.plot(ma20)
    #添加网格，可有可无，只是让图像好看点
plt.grid()
    #记得加这一句，不然不会显示图像
plt.show()

# 版权声明：本文为CSDN博主「尧十三decode」的原创文章，遵循 CC 4.0 BY-SA 版权协议，转载请附上原文出处链接及本声明。
# 原文链接：https://blog.csdn.net/sinat_42349312/article/details/83786858
plt.show()



