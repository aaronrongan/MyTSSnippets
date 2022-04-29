
import config
import pandas as pd
import matplotlib
# matplotlib.use('agg') #不可以在屏幕绘图
matplotlib.use('TkAgg') #可以在屏幕绘图
import matplotlib.pyplot as plt

import matplotlib.ticker as ticker

from Util import *

class Viewer:
    def __init__(self):
        super().__init__()

    
    @staticmethod
    def ShowBenchmarkStrategy(dfBM,dfStrategy):

        # 这两行代码解决 plt 中文显示的问题
        plt.rcParams['font.sans-serif'] = ['SimHei']
        plt.rcParams['axes.unicode_minus'] = False

        dfBM=dfBM.loc[:,'close_regular'].to_frame()
        dfBM.columns=['BenchmarkValue']
        dfBM['BenchmarkValue']=dfBM.apply(lambda x: float(x)-1,axis=1)   
        # dfBM['BenchmarkValue']=dfBM.apply(lambda x: Util.Float2Percent(x),axis=1) 
       
        # dfStrategy=dfStrategy.loc[:,['Date','MarketValue']]
        # dfStrategy.columns=['date','StrategyValue']
        # # dfStrategy.reset_index(drop=True,inplace=True)
        # dfStrategy.set_index('date',inplace=True)

        dfStrategy=dfStrategy.loc[:,['MarketValue']]
        dfStrategy.columns=['StrategyValue']
        # dfStrategy.reset_index(drop=True,inplace=True)
        # dfStrategy.set_index('date',inplace=True)

        dfStrategy['StrategyValue']=dfStrategy.apply(lambda x: float(x)-1,axis=1)   
        # dfStrategy['StrategyValue']=dfStrategy.apply(lambda x: Util.Float2Percent(x),axis=1)  

        # print(dfStrategy.head(2))
        # dfStrategy.plot()

        df=pd.concat([dfBM,dfStrategy],axis=1)

        plt.plot(df.index,df['BenchmarkValue'],label='Benchmark收益率',color='r',linewidth=1,linestyle=':')
        plt.plot(df.index,df['StrategyValue'],label='Strategy收益率',color='b',linewidth=2,linestyle='-')

        # 添加注释
        # plt.annotate('Interpolation point', xy=(x0, y0), xytext=(x0, y0 - 1), arrowprops=dict(arrowstyle='->'))  # 添加注释

        # 绘制箭头
        # for x0, y0 in zip(x, y):
        #     plt.quiver(x0, y0 - 0.3, 0, 1, color='g', width=0.005)  

        plt.ylabel('收益率') # 横坐标轴的标题
        plt.xlabel('日期') # 纵坐标轴的标题
        # plt.xticks(d)
        # plt.xticks(df.index)
        plt.legend() # 显示图例, 图例中内容由 label 定义
        plt.grid() 

        def to_percent(data, position):
            return '%1.00f'%(100*data) + '%'

        plt.gca().yaxis.set_major_formatter(ticker.FuncFormatter(to_percent))

        plt.title('收益率对比')
        plt.show()
        # Viewer.ShowBenchmarkStrategy(dfBenchmarkDailyRegular,dfDailyLogger)
