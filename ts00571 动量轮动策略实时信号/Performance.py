import config

import pandas as pd

import csv

from Util import *

import ffn

# 回测结果类，
# 盈亏比例、最大回撤、最大回测区间
# 
class Performance():
    
    def __init__(self,startdate,enddate):
        # self.theBenchmark=Benchmark()
        # self.theTarget=self.Target()
        self.ID=''      #Index号
        self.ProfitPct=1 # 参考指数收益
        self.MaxDrawdown=0 # 最大回测率
        self.TradeNumbers=0        #交易次数
        self.TradeNumbers_Pos=0     #盈利次数
        self.TradeNumbers_Neg=0     #亏损次数
        self.monthly_returns=''     #每月情况

        self.Startdate=startdate
        self.Enddate=enddate
        
        # 每天的收盘价格，和Logger文件不一样（只是有交易的记录）
        # 列名：Date  MarketValue
        # 算法是，读取Logger文件，按时间循环，每天持仓多少、现金多少，如果没有交易、没有，和
        self.TransLoggerPathName=''
        self.dfTransLogger=pd.DataFrame()

        self.DailyLoggerPathName=''
        self.dfDailyLogger=pd.DataFrame()
        self.bPrintFlag=True
        self.TradingDaysList=[]
        # if self.TradingDaysList==None:
        # self.TradingDaysList=list(map(str,config.g_DataFeeder.GetTradingDays(startdate,enddate)))
  
    
# 回测结果，简单型，分析回测，对指数进行分析，不用考虑仓位
class Performance_Simple(Performance):

    def __init__(self,startdate,enddate):
        super().__init__(startdate,enddate)
        
        # self.LoggerPathName='C:\\Users\\Aaron\\Documents\\MyMobileBooks_800_Reading\\MyTSSnippets\\ts00571 动量轮动策略实时信号\\Data_BackTest\\StrategyLogger_030_200721_214508.csv'
        
        # 最后一笔未卖出结算的IndexID，用于计算回测期间的真实价格
        self.UncheckoutIndexID=None
        self.UncheckoutIndexBuyPrice=0 #买入当时的价格

    #根据年度汇总
    def GetAnnualSummary(self):
        pass

    def GetPerformance(self):

        self.__ReadTransLoggerFile()

        self.__WriteDailyLogger(self.Startdate,self.Enddate) 

        self.__CalculatePerformance()

        
    # 通过日志文件来计算Performance
    # Logger文件格式：Date,Time,Signal,Index,Shares,Price,CurPL,CumPL
    def __CalculatePerformance(self):
        # print('sub_class')

        self.ProfitPct=1

        # 读取交易日志文件。这里的日志文件可能是个问题，将来要改。和Account放一起，类的归属有点乱，不够清晰
        # 这里还需要加入修改Logger文件功能，增加2列：当笔盈亏、累计盈亏
        

        PreviousRowSignal=self.dfTransLogger.iloc[0]['Signal']
        PreviousRowPrice=self.dfTransLogger.iloc[0]['Price']
        # print('PreviousRowSignal:' + PreviousRowSignal)
        # 第一行信号应该为"BUY"

        for index,row in self.dfTransLogger.iterrows():
            # print(row['Signal'])
            if row['Signal']=='SELL':

                if config.g_silentmode==False:   
                    print('此次交易涨幅变动：' + str((float(row['Price']))/float(PreviousRowPrice)))

                self.ProfitPct=self.ProfitPct*(float(row['Price']))/float(PreviousRowPrice)
                self.UncheckoutIndexID=None

                self.TradeNumbers=self.TradeNumbers+1
                
                if float(row['Price'])/float(PreviousRowPrice)>1:
                    self.TradeNumbers_Pos=self.TradeNumbers_Pos+1
                elif float(row['Price'])/float(PreviousRowPrice)<1:
                    self.TradeNumbers_Neg=self.TradeNumbers_Neg+1

            elif row['Signal']=='BUY':
                PreviousRowPrice=float(row['Price'])
                self.UncheckoutIndexID=row['Index']
                self.UncheckoutIndexBuyPrice=float(row['Price'])
            # if row['Signal']<>LastRowSignal:
                # print('same')
            # print(item['date'])

        # 如果最后一次是SELL，不用再计算，但是是Buy,则要计算最后一个交易日的收盘价
        if self.UncheckoutIndexID!=None:

            LastTransactionPL=self.__GetUncheckoutIndexPrice()/self.UncheckoutIndexBuyPrice

            self.ProfitPct=self.ProfitPct*LastTransactionPL

        self.ProfitPct=self.ProfitPct-1

        self.dfDailyLogger['Date'] = pd.to_datetime(self.dfDailyLogger['Date'])
        self.dfDailyLogger.set_index('Date',inplace=True)
        perf=self.dfDailyLogger['MarketValue'].calc_stats()
        self.monthly_returns=perf.monthly_returns

        if self.bPrintFlag==True:
            print('Strategy P&L:', str(Util.Float2Percent(self.ProfitPct)))
            print('Strategy 交易次数:',self.TradeNumbers )
            print('Strategy 交易盈利次数:',self.TradeNumbers_Pos)
            print('Strategy 交易盈利概率:',str(Util.Float2Percent(self.TradeNumbers_Pos/self.TradeNumbers)))
            print('Strategy 最大回撤:',str(Util.Float2Percent(self.MaxDrawdown)))
            # print('Strategy 每月收益:',self.monthly_returns)
            print('Strategy 每月收益:\n')
            perf.display_monthly_returns()

        # self.__WriteDailyLogger(self.Startdate,self.Enddate) 

    # 改进之前的算法，花费太多时间，至少4~5小时。
    def __WriteDailyLogger(self,startdate,enddate):
        self.dfDailyLogger=pd.DataFrame(columns=['Date','PositionIndex','MarketValue'])

        # TradingDaysList=config.g_DataFeeder.GetTradingDays(startdate,enddate)

        # TradingDaysList=list(map(str,TradingDaysList))
        

        DailyRowPointer=0
        TransRowPointer=0

        # for theDate in TradingDaysList:
        for theDate in self.TradingDaysList:

            theDate=self.TradingDaysList[DailyRowPointer][:10]  

            self.dfDailyLogger.loc[DailyRowPointer,'Date']=theDate

            MatchedDateNumber=self.__FindMatchRowsTransLog(theDate)
            # 当日无交易
            if MatchedDateNumber==0:
            
                # 第一行
                if DailyRowPointer==0:
                    self.dfDailyLogger.loc[DailyRowPointer,'PositionIndex']='EMPTY'
                    self.dfDailyLogger.loc[DailyRowPointer,'MarketValue']=1
                # 非第一行
                else:
                    PreviousIndex=self.dfDailyLogger.loc[DailyRowPointer-1,'PositionIndex']
                    self.dfDailyLogger.loc[DailyRowPointer,'PositionIndex']=PreviousIndex
                    # 上一行收盘空仓
                    if PreviousIndex=='EMPTY':
                        self.dfDailyLogger.loc[DailyRowPointer,'MarketValue']=self.dfDailyLogger.loc[DailyRowPointer-1,'MarketValue']
                    # 上一行收盘持仓
                    else:
                        PreviousDate=self.dfDailyLogger.loc[DailyRowPointer-1,'Date']
                        PreviousClosePrice=float(config.g_DataFeeder.GetTheDateTimeMinute10Price(PreviousIndex,PreviousDate,'15:00:00'))
                        TodayClosePrice=float(config.g_DataFeeder.GetTheDateTimeMinute10Price(PreviousIndex,theDate,'15:00:00'))
                        TodayPL=TodayClosePrice/PreviousClosePrice
                        self.dfDailyLogger.loc[DailyRowPointer,'MarketValue']=float(self.dfDailyLogger.loc[DailyRowPointer-1,'MarketValue'])*TodayPL
            
            # 当日一次买或卖       
            elif MatchedDateNumber==1:
                # 当日买
                if self.dfTransLogger.loc[TransRowPointer,'Signal']=='BUY':
                    self.dfDailyLogger.loc[DailyRowPointer,'PositionIndex']=self.dfTransLogger.loc[TransRowPointer,'Index']
                    
                    BuyPrice=float(self.dfTransLogger.loc[TransRowPointer,'Price'])
                    BuyIndex=self.dfTransLogger.loc[TransRowPointer,'Index']
                    ClosePrice=float(config.g_DataFeeder.GetTheDateTimeMinute10Price(BuyIndex,theDate,'15:00:00'))
                    # 第一行买入
                    if DailyRowPointer==0:
                        self.dfDailyLogger.loc[DailyRowPointer,'MarketValue']=ClosePrice/BuyPrice
                    # 非第一行买入
                    elif DailyRowPointer!=0:
                        self.dfDailyLogger.loc[DailyRowPointer,'MarketValue']=float(self.dfDailyLogger.loc[DailyRowPointer-1,'MarketValue'])*ClosePrice/BuyPrice

                # 当日卖
                elif self.dfTransLogger.loc[TransRowPointer,'Signal']=='SELL':
                    self.dfDailyLogger.loc[DailyRowPointer,'PositionIndex']='EMPTY'

                    SoldIndex=self.dfTransLogger.loc[TransRowPointer,'Index']
                    PreviousDate=self.dfDailyLogger.loc[DailyRowPointer-1,'Date']
                    PreviousDateClosePrice=float(config.g_DataFeeder.GetTheDateTimeMinute10Price(SoldIndex,PreviousDate,'15:00:00'))
                    SoldPrice=float(self.dfTransLogger.loc[TransRowPointer,'Price'])

                    OldPLPct=SoldPrice/PreviousDateClosePrice

                    self.dfDailyLogger.loc[DailyRowPointer,'MarketValue']=float(self.dfDailyLogger.loc[DailyRowPointer-1,'MarketValue'])*OldPLPct
                
                TransRowPointer=TransRowPointer+1

            # 当日卖当日买的情况
            elif MatchedDateNumber==2:
                
                SoldIndex=self.dfTransLogger.loc[TransRowPointer,'Index']
                PreviousDate=self.dfDailyLogger.loc[DailyRowPointer-1,'Date']
                PreviousDateClosePrice=float(config.g_DataFeeder.GetTheDateTimeMinute10Price(SoldIndex,PreviousDate,'15:00:00'))
                SoldPrice=float(self.dfTransLogger.loc[TransRowPointer,'Price'])
                OldPLPct=SoldPrice/PreviousDateClosePrice

                BuyPrice=float(self.dfTransLogger.loc[TransRowPointer+1,'Price'])
                BuyIndex=self.dfTransLogger.loc[TransRowPointer+1,'Index']
                BuyClosePrice=float(config.g_DataFeeder.GetTheDateTimeMinute10Price(BuyIndex,theDate,'15:00:00'))
                NewPLPct=BuyClosePrice/BuyPrice

                self.dfDailyLogger.loc[DailyRowPointer,'PositionIndex']=BuyIndex
                self.dfDailyLogger.loc[DailyRowPointer,'MarketValue']=self.dfDailyLogger.loc[DailyRowPointer-1,'MarketValue']*OldPLPct*NewPLPct

                TransRowPointer=TransRowPointer+2

            DailyRowPointer=DailyRowPointer+1

        # print(self.dfDailyLogger)

        # 计算最大回撤
        self.MaxDrawdown=ffn.calc_max_drawdown(self.dfDailyLogger['MarketValue'])

        self.dfDailyLogger.to_csv(self.DailyLoggerPathName,index=False,header=True)


    # 为__WriteDailyLogger编写，找出TransLogger中符合当日日期的有几个
    def __FindMatchRowsTransLog(self,theDate):
        MatchedDF=self.dfTransLogger[self.dfTransLogger['Date']==theDate]
        return len(MatchedDF)

        # return 0
    # !!!这里的算法非常麻烦，要考虑收盘价格、TransLogger和DailyLogger的转换
    # 创建DailyLogger日志文件,每一天的CumPL即可，字段：日期,CumPL
    # 同时并且获取MaxDrawdown(应该用一个标准Numpy函数计算局部波峰波谷值?)
    # 根据Logger文件，使用RowPointer方法：
    # 这个函数有点怪，是否应该放到其它类，比如Account? 不可以，因为只有在回测是才有必要，Account只针对某个交易
    # 这里的算法逻辑太乱，没有在纸上写出所有的情况。重写
    def __WriteDailyLogger2(self,startdate,enddate):

        self.dfDailyLogger=pd.DataFrame(columns=['Date','PositionIndex','MarketValue'])

        TradingDaysList=config.g_DataFeeder.GetTradingDays(startdate,enddate)
        # print(type(TradingDaysList))
        # 修改数据类型从DateTime到String
        TradingDaysList=list(map(str,TradingDaysList))
        # print(type(TradingDaysList))
        # self.dfTransLogger
        LogRowPointer=0
        DailyRowPointer=0
        PreviousRowCumPL=0
        # MiniumValue=1

        PreviousRowDate=self.dfTransLogger.iloc[0]['Date']
        PreviousRowSignal=self.dfTransLogger.iloc[0]['Signal']
        PreviousRowPrice=self.dfTransLogger.iloc[0]['Price']
        PreviousRowIndex=self.dfTransLogger.iloc[0]['Index']
        
        LoggerLength=len(self.dfTransLogger)

        # for theDate in TradingDaysList:
        while(DailyRowPointer<len(TradingDaysList)):

            theDate=TradingDaysList[DailyRowPointer][:10]  

            # theDate=theDate[:10]
            
            self.dfDailyLogger.loc[DailyRowPointer,'Date']=theDate

            print(theDate)
            print(self.dfTransLogger.iloc[LogRowPointer]['Date'])

            # 如果Logger文件中含有当日日期
            if theDate==self.dfTransLogger.iloc[LogRowPointer]['Date']:
                # if self.dfTransLogger.iloc[LogRowPointer]['Signal']=='BUY':
                
                # 需要考虑买入时价格，收盘时的价格区别
                if self.dfTransLogger.iloc[LogRowPointer]['Signal']=='BUY':
                    BuyPrice=float(self.dfTransLogger.iloc[LogRowPointer]['Price'])
                    if PreviousRowIndex!='EMPTY':
                        ClosePrice=float(config.g_DataFeeder.GetTheDateTimeMinute10Price(PreviousRowIndex,theDate,'15:00:00'))
                    else:
                        ClosePrice==float(config.g_DataFeeder.GetTheDateTimeMinute10Price(self.dfTransLogger.iloc[LogRowPointer]['Index'],theDate,'15:00:00'))

                    self.dfDailyLogger.loc[DailyRowPointer,'MarketValue']=round(float(self.dfTransLogger.iloc[LogRowPointer]['CumPL'])*(ClosePrice/BuyPrice),5)
                    self.dfDailyLogger.loc[DailyRowPointer,'PositionIndex']=self.dfTransLogger.iloc[LogRowPointer]['Index']
                    
                    # PreviousRowCumPL=float(self.dfTransLogger.iloc[LogRowPointer]['CumPL'])
                    
                    PreviousRowPrice=BuyPrice
                    PreviousRowClosePrice=ClosePrice
                    PreviousRowIndex=self.dfTransLogger.iloc[LogRowPointer]['Index']

                elif self.dfTransLogger.iloc[LogRowPointer]['Signal']=='SELL':

                    SellPrice=float(self.dfTransLogger.iloc[LogRowPointer]['Price'])

                    PreviousRowMarketValue=self.dfDailyLogger.loc[DailyRowPointer-1,'MarketValue']

                    self.dfDailyLogger.loc[DailyRowPointer,'MarketValue']=round(PreviousRowMarketValue*(SellPrice/PreviousRowClosePrice),5)

                    # self.dfDailyLogger.loc[DailyRowPointer,'PositionIndex']=self.dfTransLogger.iloc[LogRowPointer]['Index']

                    self.dfDailyLogger.loc[DailyRowPointer,'PositionIndex']='EMPTY'

                    PreviousRowIndex='EMPTY'
                    # PreviousRowPrice=SellPrice

                PreviousRowDate=self.dfTransLogger.iloc[LogRowPointer]['Date']
                PreviousRowSignal=self.dfTransLogger.iloc[LogRowPointer]['Signal']
                
    
                # 如果交易日志最后一天不是回测最后一天，后面的都按交易日志的最后一天来测试
                if LogRowPointer<LoggerLength-1:
                    # 对于下一个记录不是同一天
                    if PreviousRowDate!=self.dfTransLogger.iloc[LogRowPointer+1]['Date']:

                        LogRowPointer=LogRowPointer+1

                    # 对当日卖出再买入的进行调整
                    else:
                        PreviousDate=self.dfDailyLogger.loc[DailyRowPointer-1,'Date']

                        if PreviousRowIndex!='EMPTY':
                            PreviousDateClosePrice=float(config.g_DataFeeder.GetTheDateTimeMinute10Price(PreviousRowIndex,PreviousDate,'15:00:00'))
                        else:
                            PreviousRowIndex=self.dfDailyLogger.loc[DailyRowPointer-1,'Index']
                            PreviousDateClosePrice=float(config.g_DataFeeder.GetTheDateTimeMinute10Price(PreviousRowIndex,PreviousDate,'15:00:00'))

                        SoldPLPct=float(self.dfTransLogger.iloc[LogRowPointer]['Price'])/float(PreviousDateClosePrice)

                        NewRowSignal=self.dfTransLogger.iloc[LogRowPointer+1]['Signal']
                        NewRowIndex=self.dfTransLogger.iloc[LogRowPointer+1]['Index']
                        NewRowPrice=float(self.dfTransLogger.iloc[LogRowPointer+1]['Price'])

                        self.dfDailyLogger.loc[DailyRowPointer,'PositionIndex']=NewRowIndex
                        
                        NewRowClosePrice=float(config.g_DataFeeder.GetTheDateTimeMinute10Price(NewRowIndex,theDate,'15:00:00'))
                        
                        NewPLPct=NewRowClosePrice/NewRowPrice
                        # MarketValue=float(self.dfTransLogger.iloc[LogRowPointer]['CurPL'])*(PreviousRowClosePrice/PreviousRowPrice)
                        MarketValue= float(self.dfDailyLogger.loc[DailyRowPointer-1,'MarketValue'])*SoldPLPct*NewPLPct
                        
                        self.dfDailyLogger.loc[DailyRowPointer,'MarketValue']=round(MarketValue,5)
               
                        LogRowPointer=LogRowPointer+2

                        PreviousRowSignal=NewRowSignal
                        PreviousRowPrice=NewRowPrice
                        PreviousRowIndex=NewRowIndex
                        PreviousRowClosePrice=NewRowClosePrice

                else:
                    LogRowPointer=LogRowPointer
                    # PreviousRowClosePrice=float(config.g_DataFeeder.GetTheDateTimePrice(PreviousRowIndex,theDate,'15:00:00'))
                    # # 最大回撤
                    # if MiniumValue>PreviousRowCumPL:
                    #     MiniumValue=PreviousRowCumPL
                    # DailyRowPointer=DailyRowPointer+1
                # elif self.dfTransLogger.iloc[LogRowPointer]['Signal']=='SELL':
            
            # 如果当日无交易
            else:
                # 如果上次是BUY，本日无交易，当日市值要获取今日价格/昨日价格*前次市值
                if PreviousRowSignal=='BUY':
                    
                    TodayClosePrice=float(config.g_DataFeeder.GetTheDateTimeMinute10Price(PreviousRowIndex,theDate,'15:00:00'))
                    TodayPL=TodayClosePrice/PreviousRowClosePrice

                    PreviousRowMarketValue=round(float(self.dfDailyLogger.loc[DailyRowPointer-1,'MarketValue']),5)

                    self.dfDailyLogger.loc[DailyRowPointer,'PositionIndex']=PreviousRowIndex
                    self.dfDailyLogger.loc[DailyRowPointer,'MarketValue']=round(PreviousRowMarketValue*TodayPL,5)

                    PreviousRowClosePrice=TodayClosePrice

                # 如果上次是SELL，本日无交易，当日市值为前次市值 
                elif PreviousRowSignal=='SELL':
                    self.dfDailyLogger.loc[DailyRowPointer,'PositionIndex']='EMPTY'
                    self.dfDailyLogger.loc[DailyRowPointer,'MarketValue']=round(float(self.dfDailyLogger.loc[DailyRowPointer-1,'MarketValue']),5)

                    PreviousRowIndex='EMPTY'
                
            
            DailyRowPointer=DailyRowPointer+1
            print(self.dfDailyLogger)
        self.dfDailyLogger.to_csv(self.DailyLoggerPathName,index=False,header=True)

    # 获取未售出的股票最后一天收盘价格
    def __GetUncheckoutIndexPrice(self):
        # return float(g_DataFeeder.GetTheDateTimePrice(self.UncheckoutIndexID,self.Enddate,'15:00:00'))
        return float(config.g_DataFeeder.GetTheDateTimeMinute10Price(self.UncheckoutIndexID,self.Enddate,'15:00:00'))
    
    # 读取日志
    # 在Logger日志的最后一行添加完成记录
    def __ReadTransLoggerFile(self):
        # print(self.dfTransLogger)
        tmp_lst=[]
        iCount=0

        DataStartRow=0

        with open(self.TransLoggerPathName) as file_obj:
            
            reader = csv.reader(file_obj)

            for row in reader:
                tmp_lst.append(row)
                iCount=iCount+1
                if row[0]=='Date':
                    DataStartRow=iCount
                
        # 从第4行开始读取，这里应该用程序方法，读到Dates行的下一行开始
        self.dfTransLogger= pd.DataFrame(tmp_lst[DataStartRow:], columns=tmp_lst[DataStartRow-1]) 

        # 获取DailyLogger文件名称
        self.DailyLoggerPathName=self.TransLoggerPathName.replace('Trans','Daily')

        # print(self.dfTransLogger)  
    
    # # 读取并更新交易记录、增加2列：当笔盈亏、累计盈亏
    # def __ReadUpdateLoggerFile(self):
    #     # print(self.dfTransLogger)
    #     tmp_lst=[]
    #     # 增加表头

    #     with open(self.TransLoggerPathName) as file_obj:
            
    #         line_count=0

    #         reader = csv.reader(file_obj, delimiter=',')
    #         # 含有表头的那行增加2列, theP&L, CumP&L
            

    #         for row in reader:
    #             # 读取Logger    
    #             tmp_lst.append(row)

    #             # 更新Logger
    #             if line_count==0:
    #                 line_count=line_count+1
    #             elif line_count==1:
                    
    #                 line_count=line_count+1
    #             # else:
                    
                
    #     self.dfTransLogger= pd.DataFrame(tmp_lst[2:], columns=tmp_lst[1]) 