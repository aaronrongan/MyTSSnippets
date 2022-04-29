
import sys
sys.path.append('C:\\Users\\Aaron\\Documents\\MyMobileBooks_800_Reading\\MyTSSnippets\\CommonModules')
sys.path.append('C:\\Users\\Aaron\\Documents\\MyMobileBooks_800_Reading\\MyTSSnippets\\CommonModules\\WeChatAPIWrapper')

import config


from Account import *

from Strategy import *
from Performance import *
from Benchmark import *

import datetime

from time import *
import time
from Viewer import *

# 运行的父类，包括BackTest、RealTime、Interactive(?)
class Trading():    
    def __init__(self):

        

        # 策略返回的BUY or SELL信号，选中的index。共Account对象用；
        self.cg_Signal=''
        self.cg_SignalIndex=''
        self.cg_SignalPrice=0
        self.bPrintFlag=True


# 回测框架， 动作类
# 起始日期、结束日期
# 日线还是分钟线回测
# 每天的回测时间点 (如果是分钟线，则不用)
# 用什么策略, 用ID号010/020/030表示，根据名称动态生成类
# 结果：盈亏、最大回撤
# 测试结果的输出
class Trading_BackTest(Trading):

    def __init__(self, startdate,enddate):

        super(Trading_BackTest, self).__init__()

        self.StartDate=startdate
        self.EndDate=enddate
        self.BarType='day' # or 'minute'
        self.RunTime='14:30:00'
        # self.theStrategy=self.__CreateStrategyInstance(StrategyID) 

        self.thePerformance=Performance(self.StartDate,self.EndDate)

        self.theAccount=Account_BackTest()

        self.TradingDaysList=config.g_DataFeeder.GetTradingDays(startdate,enddate)

    
        # 交易记录文件
        self.LoggerFilePathName=''
        
        # 策略返回的BUY or SELL信号，选中的index。共Account对象用；
        self.cg_Signal=''
        self.cg_SelectedIndex=''
        self.cg_Price=0

        # __CleanAllLoggerFiles()

    # 回测前，将所有的回测文件删除
    # def __CleanAllLoggerFiles(self):
    #     self.theAccount

    # def __CreateStrategyInstance(self,StrategyID):
    #     StrategyName='Strategy' + StrategyID
    #     dynclass=globals()[StrategyName]
    #     return dynclass()

    # 每个策略运行前进行初始化，设置参数
    def __InitStrategy(self,StrategyID):
        # 动态生成策略类
        dynStrategyClass=globals()['StrategyDL' + StrategyID]
        self.theStrategy = dynStrategyClass()

        # 不打印中间输出
        self.theStrategy.bPrintFlag=False

        print('==============' + self.theStrategy.cg_StrategyName + '============')

        self.theStrategy.cg_VRDays=Util.GetVRDays(self.theStrategy.cg_VRDays)
        self.theStrategy.cg_AVDays=Util.GetAVDays(self.theStrategy.cg_AVDays)

        # print('==============' + self.theStrategy.cg_StrategyName + '============')

        self.thePerformance=Performance_Simple(self.StartDate,self.EndDate)

    # 回测模式，运行某个策略，某个日期、某个时间
    # 回测时，取N日均线涨幅，不能取当日的，比如14:30发出信号，不能用当日的15:00来回测。聚宽是用前一日的，但是实际计算应该取当日14:30的作为最新的计算
    def __RunStrategy(self,StrategyID,theDate,theTime):
        
        # 获取参数。默认值
            # self.theStrategy.cg_VRDays=Util.GetVRDays(self.theStrategy.cg_VRDays)
            # self.theStrategy.cg_AVDays=Util.GetAVDays(self.theStrategy.cg_AVDays)

        

        self.cg_Signal,self.cg_SelectedIndex,self.cg_Price=self.theStrategy.GetTransactionSignal(theDate,theTime)
        
        if self.bPrintFlag==True:
            print('时间:'+ theDate + ' ' + theTime)

        if self.cg_SelectedIndex=='ALL':
            # print(self.cg_Signal,self.cg_SelectedIndex,self.cg_Price)
            if self.bPrintFlag==True:
                print('卖出所有')
        else:
            if self.bPrintFlag==True:
                print(self.cg_Signal,self.cg_SelectedIndex,config.g_DataFeeder.GetSecurityName(self.cg_SelectedIndex),self.cg_Price)

    # 用于回测模式
    # 根据当前信号，持仓决定买入、卖出
    # 如果买入信号，读取持仓，如果空仓则买入，写入日志
    # 如果卖出信号，读取持仓，如果有则卖出，写入日志
    def __RunTransaction(self,StrategyID,theDate,theTime):
    
        # 读取当前持仓状态
    
        PositionDate, PositionTime,PositionSignal,PositionIndex,PositionShares,PositionPrice=self.theAccount.ReadPosition()

        #如果当前持仓
        if PositionIndex!='EMPTY':
            
            # 如果是卖出信号，这里只有ALL
            # 如果相同，则卖出
            # 如果不同，则提示错误
            if self.cg_Signal=='SELL':
                # begin = datetime.datetime.now()
            
                # end = datetime.datetime.now()
                # print('self.__RunTransaction(StrategyID,theDateString, self.RunTime)运行时间：' + str(end-begin))

                # begin = datetime.datetime.now()
                # PositionCurrentPrice=g_DataFeeder.GetTheDateTimePrice(PositionIndex,theDate, theTime)
                # 10分钟线
                PositionCurrentPrice=config.g_DataFeeder.GetTheDateTimeMinute10Price(PositionIndex,theDate, theTime)
                # end = datetime.datetime.now()
                # print('PositionCurrentPrice=g_DataFeeder.GetTheDateTimePrice运行时间：' + str(end-begin))

                if PositionIndex==self.cg_SelectedIndex:
                    # begin = datetime.datetime.now()

                    self.theAccount.Transact(theDate,theTime,'SELL',self.cg_SelectedIndex,1000,PositionCurrentPrice)
                    # end = datetime.datetime.now()
                    # print('self.theAccount.Transact运行时间：' + str(end-begin))

                elif self.cg_SelectedIndex=='ALL':
                    # begin = datetime.datetime.now()

                    self.theAccount.Transact(theDate,theTime,'SELL',PositionIndex,1000,PositionCurrentPrice)
                    # end = datetime.datetime.now()
                    # print('self.theAccount.Transact(theDate,theTime,SELL,运行时间：' + str(end-begin))

                else:
                    print('需要卖出的和现有仓位不符。请检查')

            # 如果是买入信号，要比较持仓和信号Index是否相同。
            
            
            elif self.cg_Signal=='BUY':
                # 如果持仓和信号相同，则提示不需买入
                if PositionIndex==self.cg_SelectedIndex:
                    if self.bPrintFlag==True:
                        print('当前已持仓:'+ PositionIndex + ' ' + config.g_DataFeeder.GetSecurityName(PositionIndex) +',不需买入')

                # 如果持仓和信号不同，先卖出当前持仓、再买入信号Index
                elif PositionIndex!=self.cg_SelectedIndex:
                    # begin = datetime.datetime.now()
                    # PositionCurrentPrice=g_DataFeeder.GetTheDateTimePrice(PositionIndex,theDate, theTime)
                    PositionCurrentPrice=config.g_DataFeeder.GetTheDateTimeMinute10Price(PositionIndex,theDate, theTime)
                    # end = datetime.datetime.now()
                    # print('PositionCurrentPrice=g_DataFeeder.GetTheDateTimePrice运行时间：' + str(end-begin))

                    self.theAccount.Transact(theDate,theTime,'SELL',PositionIndex,1000,PositionCurrentPrice)
                    

                    self.theAccount.Transact(theDate,theTime,'BUY',self.cg_SelectedIndex,1000,self.cg_Price)

                    
        #如果当前空仓
        elif PositionIndex=='EMPTY':
            
            if self.cg_Signal=='BUY':
                self.theAccount.Transact(theDate,theTime,'BUY',self.cg_SelectedIndex,1000,self.cg_Price)

            elif self.cg_Signal=='SELL':
                if self.bPrintFlag==True:
                    print('当前空仓') 

    # 运行日期循环,对每一天进行Strategy/Transaction
    # 对多个策略(错误，这个类应该只针对一个BackTest)
    # def Run(self,lstStrategyID):
    def Run(self,StrategyID,RunTime='14:30:00'):
        # self.theStrategy
        # print(self.TradingDaysList)

        # print(self.theStrategy.ETFList)

        # self.StrategyList=lstStrategyID
        
        a = datetime.datetime.strptime(self.StartDate,'%Y-%m-%d')
        b = datetime.datetime.strptime(self.EndDate,'%Y-%m-%d')
        self.RunTime=RunTime
        print('回测运行时间:',self.RunTime)

        # TradingDaysList=g_DataFeeder.GetTradingDays(self.StartDate,self.EndDate)
        
        # 这里应该先循环同一个策略，而不是先循环日期
        # for eachStrategyID in lstStrategyID:

        self.theAccount.SetPositionFileName(StrategyID)
        # self.theAccount.SetLoggerFileName(eachStrategy)
        # 这里可能有问题
        

        self.bPrintFlag=False
        # 每个策略先获取参数
        self.__InitStrategy(StrategyID)

        ParameterList=[]
        ParameterList.append(self.RunTime)
        ParameterList.append(self.theStrategy.cg_VRDays)
        ParameterList.append(self.theStrategy.cg_AVDays)
        # print(ParameterList)

        self.theAccount.CreateTransLoggerFile(StrategyID,ParameterList)

        self.theStrategy.bPrintFlag=False

        for theDate in self.TradingDaysList:
            theDateString=theDate.strftime('%Y-%m-%d')

            # begin = datetime.datetime.now()
        
            self.__RunStrategy(StrategyID,theDateString,self.RunTime)

            # end = datetime.datetime.now()
            # print('self.__RunStrategy(StrategyID,theDateString, self.RunTime)运行时间：' + str(end-begin))

            # begin = datetime.datetime.now()
            self.__RunTransaction(StrategyID,theDateString,self.RunTime)
            # end = datetime.datetime.now()
            # print('self.__RunTransaction(StrategyID,theDateString, self.RunTime)运行时间：' + str(end-begin))

            # time.sleep(g_seconds_strategyinterval)
            # time.sleep(1)
        
        # 输出该Strategy的内容
        # 打印策略各指数结果
        print('策略结束日期:',theDate)
        printDF=self.theStrategy.dfOutput
        printDF.iloc[:,2]=printDF.iloc[:,2].apply(Util.Float2Percent)
        printDF.iloc[:,3]=printDF.iloc[:,3].apply(Util.Float2Percent)
        # printDF['']
        print(printDF)

        # 完成Logger最后一天的内容，如果仍然持仓（最后一行为BUY，要计算最后一日的价格，加上内容）
        self.theAccount.FinishTransLogger(theDate.strftime('%Y-%m-%d'))

        
        
        # print(self.thePerformance.LoggerFilePathName)
        bm=Benchmark()
        bm.GetPerformance('000300.XSHG',self.StartDate,self.EndDate)
        # dfBenchmarkDaily=Benchmark().GetBenchmarkDaily('000300.XSHG',self.StartDate,self.EndDate)
        # dfBenchmarkDailyRegular=Benchmark().GetBenchmarkDailyRegular('000300.XSHG',self.StartDate,self.EndDate)
        # dfBenchmarkDailyRegular=
        # dfBenchmarkDaily.plot()
        dfBenchmarkDailyRegular=bm.dfDailyLoggerRegular

        self.thePerformance.TransLoggerPathName=self.theAccount.GetTransLoggerFilePathName()
        self.thePerformance.bPrintFlag=True
        # list(map(str,TradingDaysList))
        self.thePerformance.TradingDaysList =list(map(str,self.TradingDaysList))
        self.thePerformance.GetPerformance()
        dfDailyLogger=self.thePerformance.dfDailyLogger
      
        Viewer.ShowBenchmarkStrategy(dfBenchmarkDailyRegular,dfDailyLogger)

        # time.sleep(g_seconds_runinterval)
        # time.sleep(5)
    
    # def __FinishLogger(self,theDate):


# 实时监控， 动作类
# 起始日期、结束日期
# 日线还是分钟线回测
# 每天的回测时间点 (如果是分钟线，则不用)
# 用什么策略, 用ID号010/020/030表示，根据名称动态生成类
# 结果：盈亏、最大回撤
# 测试结果的输出
class Trading_RealTime(Trading):

    def __init__(self):
        # super().__init__()
        super(Trading_RealTime, self).__init__()
        # self.StrategyList=['010','020','030']
        self.theAccount=Account_RealTime()
        self.theStrategy=StrategyDL() #运行时动态生成子类

        # 策略返回的BUY or SELL信号，选中的index；
        self.cg_Signal=''
        self.cg_SelectedIndex=''
        self.cg_TransactPrice=0

    # 运行某个策略
    def __RunStrategy(self,StrategyID):

        # 动态生成策略类
        dynStrategyClass=globals()['StrategyDL' + StrategyID]
        self.theStrategy = dynStrategyClass()

        print('==============' + self.theStrategy.cg_StrategyName + '============')

        # 对策略进行实时交易操作：读取信号、当前持仓、写入日志

        # 获取当前时间
        theDate=datetime.datetime.today().strftime('%Y-%m-%d') # '如2020-07-16'
        theTime=time.strftime("%H:%M:%S", time.localtime()) #'如13:05:00'
                    
        self.cg_Signal,self.cg_SelectedIndex,self.cg_TransactPrice=self.theStrategy.GetTransactionSignal(theDate,theTime)

        # self.__RunTransaction(StrategyID,theDate, theTime)

    # # 用于实时监控模式、回测模式
    # # 获取当前信号，根据当前持仓决定买入、卖出
    # # 如果买入信号，读取持仓，如果空仓则买入，写入日志
    # # 如果卖出信号，读取持仓，如果有则卖出，写入日志
    # def Transaction(self, theDate,theTime):

    #     # 算法===============
    #     # GetSignal()

    #     # ReadPosition()

    #     # 进行买卖操作，并做记录：
    #     # 如果已有仓位，
    #     # 如果目前空仓，
    #     # Transact()

    #     # WriteLogger()

    #     # 获取信号BUY or SELL、买入卖出标的
    #     # 数据格式 BUY,000300.XSHG或者SELL,ALL
    #     Signal,SelectedIndex=self.theStrategy.GetTransactionSignal(theDate, theTime)

    #     # 读取当前持仓状态
    #     CurrentPosition=self.theAccount.ReadPosition()

    #     #如果当前持仓
    #     if CurrentPosition!='EMPTY':
            
    #         PositionIndex,PositionShares=CurrentPosition

    #         if Signal=='SELL':
    #             if PositionIndex==SelectedIndex:
    #                 self.theAccount.Transact('SELL',SelectedIndex,1000)
    #             else:
    #                 print('需要卖出的和现有仓位不符。请检查')

    #         elif Signal=='BUY':

    #             print('当前已持仓，不需买入')

    #     #如果当前空仓
    #     else:
            
    #         if Signal=='BUY':
    #             self.theAccount.Transact('BUY',SelectedIndex,1000)

    #         elif Signal=='SELL':
    #             print('当前无仓位，无需卖出')   

    # 用于实时监控模式
    # 根据当前信号，持仓决定买入、卖出
    # 如果买入信号，读取持仓，如果空仓则买入，写入日志
    # 如果卖出信号，读取持仓，如果有则卖出，写入日志
    def __RunTransaction(self,StrategyID,theDate,theTime):
        
        self.theAccount.SetPositionFileName(StrategyID)
        self.theAccount.SetLoggerFileName(StrategyID)

        # 算法===============
        # GetSignal()

        # ReadPosition()

        # 进行买卖操作，并做记录：
        # 如果已有仓位，
        # 如果目前空仓，
        # Transact()

        # WriteLogger()

        # 获取信号BUY or SELL、买入卖出标的
        # 数据格式 BUY,000300.XSHG或者SELL,ALL
        # Signal,SelectedIndex=self.theStrategy.GetTransactionSignal(theDate, theTime)

        # 读取当前持仓状态
        # CurrentPosition=

        PositionDate,PositionTime,PositionSignal,PositionIndex,PositionShares,PositionPrice=self.theAccount.ReadPosition()

        #如果当前持仓
        if PositionIndex!='EMPTY':
            
            if self.cg_Signal=='SELL':
                if PositionIndex==self.cg_SelectedIndex:
                    self.theAccount.Transact(theDate,theTime,'SELL',self.cg_SelectedIndex,1000,self.cg_TransactPrice)
                    outputstring='卖出:'+ PositionIndex + ' ' + config.g_DataFeeder.GetSecurityName(PositionIndex) + ',' +self.cg_TransactPrice
                    print(outputstring)
                    config.g_wechat.SendWeChatMessage(outputstring)
                else:
                    print('需要卖出的和现有仓位不符。请检查')

            elif self.cg_Signal=='BUY':
                if self.bPrintFlag==True:
                    outputstring='当前已持仓:'+ PositionIndex + ' ' + config.g_DataFeeder.GetSecurityName(PositionIndex) 
                    print(outputstring)
                # g_wechat.SendWeChatMessage(outputstring)
                # print('当前已持仓，不需买入')

        #如果当前空仓
        else:
            
            if self.cg_Signal=='BUY':
                
                self.theAccount.Transact(theDate,theTime,'BUY',self.cg_SelectedIndex,1000,self.cg_TransactPrice)
                
                if self.bPrintFlag==True:
                    outputstring='买入:'+ self.cg_SelectedIndex + ' ' + config.g_DataFeeder.GetSecurityName(self.cg_SelectedIndex) + ',' + str(self.cg_TransactPrice)
                
                    print(outputstring)

                config.g_wechat.SendWeChatMessage(outputstring)

            elif self.cg_Signal=='SELL':
                if self.bPrintFlag==True:
                    print('当前空仓，不需卖出')   

    def Run(self,lstStrategyID):
        
        self.StrategyList=lstStrategyID

        while(1):
            # today=time.strftime("%Y-%m-%d",time.localtime(time.time()))
            # time_stamp = datetime.datetime.now()
            thedate=datetime.datetime.today().strftime('%Y-%m-%d')
            thetime=time.strftime("%H:%M:%S", time.localtime()) 

            # if Util.IsTradingDays
            if Util.IsTradingDays(thedate)==False:
                # time.sleep(300)
                print('非交易日')
                exit()
                # continue
            else:
                # if Util.IsWorkingHours()==False:
                    # time.sleep(100)
                if Util.IsBeforeBell():
                    print('等待开盘。。。')
                    time.sleep(10)
                    continue
                elif Util.IsAfterBell():
                    print('已收盘。请等待下次开盘。')
                    exit()
                else:
                    if g_WechatSwitchOn==False:
                        AskWechatOn=Input('是否启动微信：0.不启动；1.启动；[0]')
                        if AskWechatOn=='':
                            AskWechatOn='0'

                        if AskWeChatOn=='1':
                            config.g_wechat=WeChatAPIWrapper.WeChatAPIWrapper()
                            
                            config.g_wechat.Start()
                            
                            CurrentDateTime=Util.GetLongDateTime()
                            config.g_wechat.SendWeChatMessage(CurrentDateTime + ': ts00571 starting...')

                            config.g_WechatSwitchOn=True
 
                    for eachStrategy in self.StrategyList:
                        
                        # 程序执行时间：
                        # begin = datetime.datetime.now()
                    
                        self.__RunStrategy(eachStrategy)
                        
                        self.__RunTransaction(eachStrategy,thedate, thetime)

                        # end = datetime.datetime.now()

                        # 
                        
                        # print('__RunStrategy & __RunTransaction 运行时间:' + str(end-begin))

                        time.sleep(config.g_seconds_strategyinterval)
            
            time.sleep(config.g_seconds_runinterval)

# ！！！能否集中到Trading_BackTest上
# Trading_BackTest的子类
# 起始日期、结束日期
# 日线还是分钟线回测
# 每天的回测时间点 (如果是分钟线，则不用)
# 用什么策略, 用ID号010/020/030表示，根据名称动态生成类
# 结果：盈亏、最大回撤
# 测试结果的输出
class Trading_Optimizer(Trading_BackTest):

    def __init__(self, startdate,enddate,ParaList):

        super(Trading_Optimizer, self).__init__(startdate,enddate)

        self.StartDate=startdate
        self.EndDate=enddate
        self.BarType='day' # or 'minute'
        # self.RunTime='14:30:00'
        self.RunTime=''
           
        self.thePerformance=Performance(self.StartDate,self.EndDate)

        self.theAccount=Account_Optimizer()

        # self.TradingDaysList=config.g_DataFeeder.GetTradingDays(startdate,enddate)

        # 交易记录文件
        self.LoggerFilePathName=''
        
        # 策略返回的BUY or SELL信号，选中的index。共Account对象用；
        self.cg_Signal=''
        self.cg_SelectedIndex=''
        self.cg_Price=0

        self.Para1=ParaList[0]
        self.Para2=ParaList[1]

    
    # 每个策略运行前进行初始化，设置参数
    def __InitStrategy(self,StrategyID,ParameterLists):
        # 动态生成策略类
        dynStrategyClass=globals()['StrategyDL' + StrategyID]
        self.theStrategy = dynStrategyClass()

        # print('==============' + self.theStrategy.cg_StrategyName + '============')

        self.thePerformance=Performance_Simple(self.StartDate,self.EndDate)

        self.theStrategy.bPrintFlag=False

        self.theStrategy.RunTime=ParameterLists[0]
        self.theStrategy.cg_VRDays=int(ParameterLists[1])
        self.theStrategy.cg_AVDays=int(ParameterLists[2])

    # 回测模式，运行某个策略，某个日期、某个时间
    # 回测时，取N日均线涨幅，不能取当日的，比如14:30发出信号，不能用当日的15:00来回测。聚宽是用前一日的，但是实际计算应该取当日14:30的作为最新的计算
    def __RunStrategy(self,StrategyID,theDate,theTime):
        
     
        self.cg_Signal,self.cg_SelectedIndex,self.cg_Price=self.theStrategy.GetTransactionSignal(theDate,theTime)
        
        if self.bPrintFlag==True:
            print('时间:'+ theDate + ' ' + theTime)

        if self.cg_SelectedIndex=='ALL':
            # print(self.cg_Signal,self.cg_SelectedIndex,self.cg_Price)
            if self.bPrintFlag==True:
                print('卖出所有')
        else:
            if self.bPrintFlag==True:
                print(self.cg_Signal,self.cg_SelectedIndex,config.g_DataFeeder.GetSecurityName(self.cg_SelectedIndex),self.cg_Price)

    # 用于回测模式
    # 根据当前信号，持仓决定买入、卖出
    # 如果买入信号，读取持仓，如果空仓则买入，写入日志
    # 如果卖出信号，读取持仓，如果有则卖出，写入日志
    def __RunTransaction(self,StrategyID,theDate,theTime):
    
        PositionDate, PositionTime,PositionSignal,PositionIndex,PositionShares,PositionPrice=self.theAccount.ReadPosition()

        #如果当前持仓
        if PositionIndex!='EMPTY':
            
            # 如果是卖出信号，这里只有ALL
            # 如果相同，则卖出
            # 如果不同，则提示错误
            if self.cg_Signal=='SELL':
                
                PositionCurrentPrice=config.g_DataFeeder.GetTheDateTimeMinute10Price(PositionIndex,theDate, theTime)
               
                if PositionIndex==self.cg_SelectedIndex:
                  
                    self.theAccount.Transact(theDate,theTime,'SELL',self.cg_SelectedIndex,1000,PositionCurrentPrice)
                   
                elif self.cg_SelectedIndex=='ALL':
                
                    self.theAccount.Transact(theDate,theTime,'SELL',PositionIndex,1000,PositionCurrentPrice)
                   
                else:
                    print('需要卖出的和现有仓位不符。请检查')

            # 如果是买入信号，要比较持仓和信号Index是否相同。 
            elif self.cg_Signal=='BUY':
                # 如果持仓和信号相同，则提示不需买入
                if PositionIndex==self.cg_SelectedIndex:
                    if self.bPrintFlag==True:
                        print('当前已持仓:'+ PositionIndex + ' ' + config.g_DataFeeder.GetSecurityName(PositionIndex) +',不需买入')

                # 如果持仓和信号不同，先卖出当前持仓、再买入信号Index
                elif PositionIndex!=self.cg_SelectedIndex:
                    # begin = datetime.datetime.now()
                    # PositionCurrentPrice=g_DataFeeder.GetTheDateTimePrice(PositionIndex,theDate, theTime)
                    PositionCurrentPrice=config.g_DataFeeder.GetTheDateTimeMinute10Price(PositionIndex,theDate, theTime)
                    # end = datetime.datetime.now()
                    # print('PositionCurrentPrice=g_DataFeeder.GetTheDateTimePrice运行时间：' + str(end-begin))

                    self.theAccount.Transact(theDate,theTime,'SELL',PositionIndex,1000,PositionCurrentPrice)
                    
                    self.theAccount.Transact(theDate,theTime,'BUY',self.cg_SelectedIndex,1000,self.cg_Price)

                    
        #如果当前空仓
        elif PositionIndex=='EMPTY':
            
            if self.cg_Signal=='BUY':
                self.theAccount.Transact(theDate,theTime,'BUY',self.cg_SelectedIndex,1000,self.cg_Price)

            elif self.cg_Signal=='SELL':
                if self.bPrintFlag==True:
                    print('当前空仓') 

    # 运行日期循环,对每一天进行Strategy/Transaction
    # 对多个策略(错误，这个类应该只针对一个BackTest)
    # def Run(self,lstStrategyID):
    def Run(self,StrategyID,ParameterList):

        self.bPrintFlag=False

        a = datetime.datetime.strptime(self.StartDate,'%Y-%m-%d')
        b = datetime.datetime.strptime(self.EndDate,'%Y-%m-%d')

        self.theAccount.SetPositionFileName(StrategyID)
        self.theAccount.CleanPositionFile(StrategyID)

        # self.theAccount.SetLoggerFileName(eachStrategy)
        # 这里可能有问题
        
        self.theAccount.CreateTransLoggerFile(StrategyID,ParameterList)

        self.RunTime=ParameterList[0]

        # 每个策略先获取参数
        self.__InitStrategy(StrategyID,ParameterList)

        for theDate in self.TradingDaysList:
            theDateString=theDate.strftime('%Y-%m-%d')

            # begin = datetime.datetime.now()
        
            self.__RunStrategy(StrategyID,theDateString, self.RunTime)

            # end = datetime.datetime.now()
            # print('self.__RunStrategy(StrategyID,theDateString, self.RunTime)运行时间：' + str(end-begin))

            # begin = datetime.datetime.now()
            self.__RunTransaction(StrategyID,theDateString, self.RunTime)
            
        if self.bPrintFlag==True:
            # 输出该Strategy的内容
            # 打印策略各指数结果
            print('当前日期:',theDate)
            printDF=self.theStrategy.dfOutput
            printDF.iloc[:,2]=printDF.iloc[:,2].apply(Util.Float2Percent)
            printDF.iloc[:,3]=printDF.iloc[:,3].apply(Util.Float2Percent)
            # printDF['']
            print(printDF)

        # 完成Logger最后一天的内容，如果仍然持仓（最后一行为BUY，要计算最后一日的价格，加上内容）
        self.theAccount.FinishTransLogger(theDate.strftime('%Y-%m-%d'))

        bm=Benchmark()
        bm.bPrintFlag=False
        bm.GetPerformance('000300.XSHG',self.StartDate,self.EndDate)
        # self.thePerformance.DailyLoggerFilePathName=self.theAccount.GetLoggerFilePathName()
        # self.thePerformance.TransLoggerFilePathName=self.theAccount.GetLoggerFilePathName()
        
        # print(self.thePerformance.LoggerFilePathName)
        
        self.thePerformance.TransLoggerPathName=self.theAccount.GetTransLoggerFilePathName()
        self.thePerformance.bPrintFlag=False
        self.thePerformance.TradingDaysList =list(map(str,self.TradingDaysList))
        self.thePerformance.GetPerformance()

        