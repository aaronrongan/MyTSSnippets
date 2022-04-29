import config 
import pandas as pd

from functools import reduce

from Trading import Trading_BackTest,Trading_Optimizer

from Util import Util

import os

import glob

from Benchmark import *

# 用于找出最佳的参数
# 买卖时间点
# 参数组合

class Optimizer():
    def __init__(self,StartDate,EndDate):
        
        self.Para1=[]   # Time
        self.Para2=[]   # VR_Dates参数
        self.Para3=[]   # AV_Dates参数

        self.StartDate=StartDate
        self.EndDate=EndDate
        self.StrategyID='010'

        self.RunTime=''

        # for theruntime in ['9:40:00','10:30:00','11:30:00','13:30:00','14:30:00']:
        #     self.Para1.append(theruntime)
        # self.Para1=['09:40:00','10:00:00','10:30:00','11:00:00','11:30:00','13:10:00','13:30:00','14:00:00','14:30:00','15:00:00']
        # self.Para1=['09:40:00','10:30:00','11:30:00','13:30:00','14:30:00']
        # self.Para1=['11:30:00','14:30:00']
        self.Para1=['14:30:00']

        for i in range(4,30, 3):
            self.Para2.append(i)
        
        for i in range(4,30, 3):
            self.Para3.append(i)
  
        self.ParaList=self.__GetParameterCombinations([self.Para1,self.Para2,self.Para3])

        self.theTrading=Trading_Optimizer(self.StartDate,self.EndDate,self.ParaList)

        # PerformanceList,每个回测结果的存放
        # self.thePerformanceDF=pd.DataFrame(columns=['VRDate','AVDate','P&L','MaxDrawdown','TradeNumbers','TradeWinPercent'])
        self.thePerformanceDF=pd.DataFrame(columns=['RunTime','VRDate','AVDate','P&L','MaxDrawdown','TradeNumbers','TradeWinPercent'])

        self.DataFilePath=config.g_Data_Optimizer

        # print(self.thePerformanceDF)
        
        
    def __GetParameterCombinations(self,alllists):

        FuncCombination = lambda x, code=',': reduce(lambda x, y: [str(i)+code+str(j) for i in x for j in y], x)
        
        return FuncCombination(alllists,',')

    # 将多次回测结果导出到文件，格式
    def __WritePerformanceList(self,StrategyID):
        
        pass

    # 将中间产生的Daily/Trans文件删除
    def __CleanDailyTransLogFiles(self):
        os.chdir(self.DataFilePath)
        for file in glob.glob('*Logger*'):
            os.remove(file)

    def GetBestParameters(self):

        iDFRow=0

        # 打印Benchmark
        bm=Benchmark()
        bm.bPrintFlag=True
        bm.GetPerformance('000300.XSHG',self.StartDate,self.EndDate)

        # StrategyID='010'
            # StrategyID
        # 计算每种参数组合
        for eachList in self.ParaList:
            # print(each)
            parameters=eachList.split(',')
            # for eachPara in parameters:
            #     print(eachPara)

            RunTime=parameters[0]
            VR_Date=parameters[1]
            AV_Date=parameters[2]

            
            self.theTrading.bPrintFlag=False
            self.theTrading.Run(self.StrategyID,parameters)

            # pdrow=pd.Series({})
            # self.thePerformanceDF
            self.thePerformanceDF.loc[iDFRow,'RunTime']=RunTime
            self.thePerformanceDF.loc[iDFRow,'VRDate']=VR_Date
            self.thePerformanceDF.loc[iDFRow,'AVDate']=AV_Date
            self.thePerformanceDF.loc[iDFRow,'P&L']=str(Util.Float2Percent(self.theTrading.thePerformance.ProfitPct)) #盈亏
            self.thePerformanceDF.loc[iDFRow,'MaxDrawdown']=self.theTrading.thePerformance.MaxDrawdown  # 最大回撤
            self.thePerformanceDF.loc[iDFRow,'TradeNumbers']=self.theTrading.thePerformance.TradeNumbers
            self.thePerformanceDF.loc[iDFRow,'TradeWinPercent']=Util.Float2Percent(self.theTrading.thePerformance.TradeNumbers_Pos/self.theTrading.thePerformance.TradeNumbers)

            iDFRow=iDFRow+1
        #
        print(self.thePerformanceDF)

        thedatetime=Util.GetShortDateTime()

        PerformanceListFileName=os.path.join(config.g_Data_Optimizer,'PerformanceList_' + self.StrategyID + '_'+thedatetime +'.csv')

        self.thePerformanceDF.to_csv(PerformanceListFileName)

        self.__CleanDailyTransLogFiles()

        # self.__WritePerformanceList('010')

# if __name__=='__main__':
#     theOptimizer=Optimizer('2020-01-01','2020-07-31')

#     theOptimizer.GetBestParameters()


    # print(theOptimizer.ParaList)

