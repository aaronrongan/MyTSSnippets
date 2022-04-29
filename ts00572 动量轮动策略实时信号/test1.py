# DataFrame的显示，比如DailyLogger,X轴、Y轴设置
# 和Benchmark的同时显示

import numpy as np

import pandas as pd

import matplotlib.pyplot as plt

df =pd.read_csv("C:/Users/aaron/Documents/MyMobileBooks_800_Reading/MyTSSnippets/ts00571 动量轮动策略实时信号/Data_BackTest/StrategyDailyLogger_010_200809_095447.csv")

# print(df)
df.plot()
plt.show()