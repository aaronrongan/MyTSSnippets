import sys
sys.path.append('C:\\Users\\Aaron\\Documents\\MyMobileBooks_800_Reading\\MyTSSnippets\\CommonModules')
sys.path.append('C:\\Users\\Aaron\\Documents\\MyMobileBooks_800_Reading\\MyTSSnippets\\CommonModules\\WeChatAPIWrapper')


import config

import pandas as pd 

from Util import Util

# 为一些数据类提供更直接的表示，如Benchmark、Account、
from dataclasses import dataclass

from DataFeeder import *

import matplotlib.pyplot as plt

from Viewer import *

import ffn

from empyrical import max_drawdown 

# 仅作为属性用，不用再加入方法
@dataclass
class Benchmark:
    # def __init__(self):
    #     self.ID=''      #Index号
    #     self.ProfitPct=1 # 参考指数收益
    #     self.MaxDrawdown=0 # 最大回测率
    #     print('sub_class')
    IndexID: str =''
    ProfitPct: float = 1
    MaxDrawdown: float =0
    dfDailyLogger:pd.DataFrame =pd.DataFrame()
    dfDailyLoggerRegular:pd.DataFrame =pd.DataFrame()
    bPrintFlag : bool =True

    # def SetBenchmark(self):
    #     self.IndexID=IndexID

    # 获取该BenchMark的收益值
    # @staticmethod
    # def GetPerformance(self,Index,startdate,enddate):
    def GetPerformance(self,Index,startdate,enddate):
        
        self.__GetBenchmarkDailyRegular(Index,startdate,enddate)

        # 获取实际的开始日期，比如不算开始时间是假日
        # startdate=Util.GetCloseAfterTradingDate(startdate)

        # 要计算实际开始日期的前一个交易日
        startprice=1
        # print(startprice)
        endprice=self.dfDailyLoggerRegular['close_regular'][-1:]
        # print(endprice)

        # actualstartdate=Util.GetDeltaTradingDate(startdate,-1)
        # startprice=config.g_DataFeeder.GetTheDateTimeMinute10Price(Index,actualstartdate,'15:00:00')
        # endprice=config.g_DataFeeder.GetTheDateTimeMinute10Price(Index,enddate,'15:00:00')

        # startprice=config.g_JQDataFeeder.GetTheDateTimePrice(Index,actualstartdate,' 15:00:00')
        # endprice=config.g_JQDataFeeder.GetTheDateTimePrice(Index,enddate,' 15:00:00')
        

        # startprice=JQDataInterface.GetTheDateTimePrice('000300.XSHG','2020-06-01')

        self.ProfitPct=endprice/startprice-1

        # print('Benchmark P&L:' + str(self.ProfitPct-1))
        Util.Float2Percent(self.ProfitPct-1)

        if self.bPrintFlag==True:
            print('Benchmark P&L:' + Util.Float2Percent(self.ProfitPct))
            print('Benchmark 最大回撤:',str(Util.Float2Percent(self.MaxDrawdown)))
        
        # 最大回撤计算，每天的循环

        return self.ProfitPct
    
    # 对指数进行归一化处理，如4000多点、、、都用1/1.05/...表示
    # 需要知道前一天的收盘数据
    def __GetBenchmarkDailyRegular(self,Index,startdate,enddate):

        # config.g_T
        PreviousDate=Util.GetDeltaTradingDate(startdate,-1)

        PreviousDayClosePrice=config.g_DataFeeder.GetTheDateTimeMinute10Price(Index,PreviousDate,'15:00:00')

        self.dfDailyLoggerRegular=config.g_DataFeeder.GetDayPriceBarbySE(Index,startdate,enddate)  

        # for theDate in dfDailyLoggerRegular:
        self.dfDailyLoggerRegular['close_regular']=self.dfDailyLoggerRegular.apply(lambda x: x['close']/PreviousDayClosePrice,axis=1)    
        # print(self.dfDailyLoggerRegular)

        self.MaxDrawdown=ffn.calc_max_drawdown(self.dfDailyLoggerRegular['close_regular'])

        # return self.dfDailyLoggerRegular
        

    # 返回Dataframe，格式：日期、累计
    def GetBenchmarkDaily(self,Index,startdate,enddate):

        # dfBenchmarkDaily=pd.DataFrame(columns=['Date','PositionIndex','MarketValue'])

        # TradingDaysList=config.g_DataFeeder.GetTradingDays(startdate,enddate)

        # TradingDaysList=list(map(str,TradingDaysList))

        # DailyRowPointer=0
        # TransRowPointer=0

        # for theDate in TradingDaysList:
        self.dfDailyLogger=config.g_DataFeeder.GetDayPriceBarbySE(Index,startdate,enddate)  

    
        return self.dfDailyLogger


if __name__=='__main__':
    if config.g_DataFeeder==None:
        config.g_DataFeeder=LocalDataFeederMemory()
    # df=Benchmark().GetBenchmarkDaily('000300.XSHG','2020-07-01','2020-07-31')['close']
    # print(df)     
    dfBM=Benchmark().GetBenchmarkDailyRegular('000300.XSHG','2020-07-01','2020-07-31').loc[:,'close'].to_frame()
    # dfBM.reset_index(drop=True,inplace=True)
    dfBM.columns=['BenchmarkValue']
    eachdayReturn=ffn.to_returns(dfBM['BenchmarkValue'])
    print(eachdayReturn)
    print(max_drawdown(eachdayReturn))
    
    print(ffn.calc_max_drawdown(dfBM['BenchmarkValue']))

    

    # dfStrategy =pd.read_csv("C:/Users/aaron/Documents/MyMobileBooks_800_Reading/MyTSSnippets/ts00571 动量轮动策略实时信号/Data_BackTest/StrategyDailyLogger_010_200809_095447.csv")
    
    # dfStrategy=dfStrategy.loc[:,['Date','MarketValue']]
    # dfStrategy.columns=['date','StrategyValue']
    # dfStrategy.reset_index(drop=True,inplace=True)
    # dfStrategy.set_index('date',inplace=True)
    # print(dfStrategy.head(2))
    # dfStrategy.plot()

    # Viewer.ShowBenchmarkStrategy(dfBenchmarkDailyRegular,dfDailyLogger)

    # df=pd.concat([dfBM,dfStrategy],axis=1)
    # print(df)
    # df.plot()
    # plt.show()

    

