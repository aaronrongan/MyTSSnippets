import tushare as ts
import pandas as pd
import seaborn as sns

# 设置token，只需要在第一次调用或者token失效时设置
# 设置完成后，之后就不再需要这一个命令了
# ts.set_token('*******')
token='f20927201ecc20e3cea9279abacfbb1d39a9624820d9b2f94613f722'

pro=ts.pro_api(token)

df_daily = pro.index_daily(ts_code="000001.SH")
df_daily.head()

df_daily.index = pd.to_datetime(df_daily['trade_date'])
df_daily.index[:5]


# 设置为seaborn的样式，更美观
sns.set()

# 绘制收盘价曲线
df_daily.plot(y="close")

import matplotlib.pyplot as plt

df_daily = df_daily.sort_index(ascending=True)
plt.figure(figsize=(12, 6))
df_daily.close['20150101':].plot()
df_daily.close.rolling(60).mean()['20150101':].plot();

plt.show()