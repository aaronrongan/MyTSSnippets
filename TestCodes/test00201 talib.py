#ta-lib实例

#作者：CuteHand
#链接：https://zhuanlan.zhihu.com/p/57389880
#来源：知乎
#著作权归作者所有。商业转载请联系作者获得授权，非商业转载请注明出处。

#在Conda/Python 3.5中报错，找不到指定模块。
#在Python3.7.4中通过

#先引入后面可能用到的包（package） 
import pandas as pd 
import numpy as np 
import matplotlib.pyplot as plt 
#%matplotlib inline #正常显示画图时出现的中文和负号 
from pylab import mpl 
mpl.rcParams['font.sans-serif']=['SimHei'] 
mpl.rcParams['axes.unicode_minus']=False 

#引入TA-Lib库 
import talib as ta
#查看包含的技术指标和数学运算函数 
#print(ta.get_functions()) 
#print(ta.get_function_groups()) 

ta_fun=ta.get_function_groups() 
ta_fun.keys() 

#使用tushare获取上证指数数据作为示例 
import tushare as ts 
df=ts.get_k_data('sh',start='2000-01-01') 
df.index=pd.to_datetime(df.date) 
df=df.sort_index() 
types=['SMA','EMA','WMA','DEMA','TEMA', 'TRIMA','KAMA','MAMA','T3'] 
df_ma=pd.DataFrame(df.close) 

for i in range(len(types)): 
    df_ma[types[i]]=ta.MA(df.close,timeperiod=5,matype=i) 

df_ma.tail() 
df_ma.loc['2010-08-01':].plot(figsize=(16,6)) 
ax = plt.gca() 
ax.spines['right'].set_color('none') 
ax.spines['top'].set_color('none') 
plt.title('上证指数各种类型移动平均线',fontsize=15) 
plt.xlabel('') 
plt.show()

################################
#画5、30、120、250指数移动平均线 
N=[5,30,120,250] 
for i in N: 
    df['ma_'+str(i)]=ta.EMA(df.close,timeperiod=i) 
df.tail() 

df.loc['2014-01-01':,['close','ma_5','ma_30','ma_120','ma_250']].plot(figsize=(16,6)) 
ax = plt.gca() 
ax.spines['right'].set_color('none') 
ax.spines['top'].set_color('none') 
plt.title('上证指数走势',fontsize=15) 
plt.xlabel('') 
plt.show()

#####
#布林带绘制范例、趋势线、抛物线及其它指标范例参考知乎原文

#均线策略回测、布林带策略回测、参考知乎原文