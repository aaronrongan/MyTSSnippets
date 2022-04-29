
import sys
# sys.path.append('C:\\Users\\Aaron\\Documents\\MyMobileBooks_800_Reading\\MyTSSnippets\\CommonModules')
sys.path.append('C:\\Users\\Aaron\\Documents\\MyMobileBooks_800_Reading\\MyTSSnippets\\ts00571 动量轮动策略实时信号')


import pandas as pd
from DataFeeder import JQDataFeeder
import csv
# from time import *
import time as t
from datetime import *
import os
from Util import *
import config

# 本地数据维护类
# 下载、更新日线数据、分钟数据
# 下载、更新所有上市代码

class DataMaintain():

    def __init__(self):
        self.DayBarPath = config.g_DayBarPath #'C:/Users/Aaron/Documents/MyMobileBooks_800_Reading/MyTSSnippets/DataRepository/db00071/Day'
        self.MinuteBarPath =config.g_MinuteBarPath #'C:/Users/Aaron/Documents/MyMobileBooks_800_Reading/MyTSSnippets/DataRepository/db00071/Minute'
        self.Minute10BarPath = config.g_Minute10BarPath #'C:/Users/Aaron/Documents/MyMobileBooks_800_Reading/MyTSSnippets/DataRepository/db00071/Minute10'
        self.IndexListCSVPathName=config.g_IndexListCSVPathName #'C:/Users/Aaron/Documents/MyMobileBooks_800_Reading/MyTSSnippets/DataRepository/db00071/IndexList.csv'
        self.TradingDaysPathName=config.g_TradingDaysPathName # 'C:/Users/aaron/Documents/MyMobileBooks_800_Reading/MyTSSnippets/DataRepository/db00131/tradingdays.csv'

        self.StockCodeListPathName=config.g_StockCodeListPathName

        self.dfIndex=pd.DataFrame()
        self.defaultDayStartDate='2006-01-01'
        self.defaultMinuteStartDate='2020-01-01'
        self.defaultMinute10StartDate='2015-01-01' # 10分钟线数据库

        # self.defaultDayStartDate='2020-07-01'
        # self.defaultMinuteStartDate='2020-07-01'
        # self.defaultMinute10StartDate='2020-07-01' # 10分钟线数据库

        # 判断是否今日3点半后
        self.bIsAfterBell=Util.IsAfterBell()
        # self.TodayDate=Util.GetTodayDateString()

    def RunMaintain(self):

        self.__GetIndexList()
       
        # todaydate='2020-07-23'

        # theDateTime=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

        self.__RunTradingDaysMaintenance()

        # self.__RunCodeListMaintenance()

        for index in self.dfIndex['IndexID']:

            self.__RunDayBarMaintenance(index)

            self.__RunMinuteBarMaintenance(index)

            self.__RunMinute10BarMaintenance(index)

    # 上市公司代码，一个季度维护一次？
    def __RunCodeListMaintenance(self):

        df=JQDataFeeder().GetCodeList('stock')
        
        df.reset_index(drop=True,inplace=True)

        if not os.path.exists(self.TradingDaysPathName):
            df.to_csv(self.StockCodeListPathName, mode='a',sep=',',  header=True, index=False)

        # To do: 如果存在文件，如何增加？用DataFrame的方法？
        # else:
        #     df.to_csv(self.StockCodeListPathName, mode='a',sep=',', header=False,  index=False)

            # .to_csv('c://1.csv',mode='a',sep=',',  header=True, index=False)

    # 日线维护
    def __RunDayBarMaintenance(self,index):
        # 新加日期用已有时间的最后一天
        startdate=self.__GetExistingEndDate(index,'d')


        if startdate==None:
            startdate=self.defaultDayStartDate
        else:
        
            startdate=self.__GetDeltaDate(startdate,1)
            
        # 当前日期，JQData库对于日线包含数据
        enddate=t.strftime("%Y-%m-%d", t.localtime()) 
        # enddate='2020-07-23'
        
        

        self.FetchBar2CSV(index,startdate,enddate,'d')


    # 获取一个日期字符串格式的偏置日期，一般用于某个日期的第二天
    def __GetDeltaDate(self,olddatestring,deltacount):
        # 在现有库的日期前增加一天日期
        olddate=datetime.datetime.strptime(olddatestring,'%Y-%m-%d')
        offset = datetime.timedelta(deltacount)
        return((olddate + offset).strftime('%Y-%m-%d'))

    # 10分钟线维护
    def __RunMinute10BarMaintenance(self,index):

        
        minutestartdate=self.__GetExistingEndDate(index,'m10')
        # print(minutestartdate)

        # 当前时间的明天，因为JQData当天日期只算到本日凌晨，要放当前日期的第二天，这样才能取到当前日期的数据。
        # 比如周五下午5点取日线数据，要放第二天，才能取到周五的数据
        # 如果是15:30前，在现有库的最新日期前增加一天日期开始算起
        # 如果是15:30后，以当日计算
        minuteenddate=self.__GetDeltaDate(t.strftime("%Y-%m-%d", t.localtime()),1)

        # if Util.IsAfterBell()==False:
        #     minuteenddate=self.__GetDeltaDate(minuteenddate,-1)

        if minutestartdate==None:
            minutestartdate=self.defaultMinute10StartDate
        else:
            # 返回格式是2020-07-23 09:31:00,所以要取前10位
            minutestartdate=self.__GetExistingEndDate(index,'m10')[:10]

            # 在现有库的日期前增加一天日期
            minutestartdate=self.__GetDeltaDate(minutestartdate,1)
            
            # minutestartdate=datetime.datetime.strptime(minutestartdate,'%Y-%m-%d')
            # offset = datetime.timedelta(1)
            # minutestartdate=(minutestartdate + offset).strftime('%Y-%m-%d')

        # self.FetchMinuteBar2CSV(index,minutestartdate,enddate)v
        self.FetchBar2CSV(index, minutestartdate,minuteenddate,BarType='m10')

    # 分钟线维护
    def __RunMinuteBarMaintenance(self,index):

        
        minutestartdate=self.__GetExistingEndDate(index,'m')
        # print(minutestartdate)

        # 当前时间的明天，因为JQData当天日期只算到本日凌晨，要放当前日期的第二天，这样才能取到当前日期的数据。
        # 比如周五下午5点取日线数据，要放第二天，才能取到周五的数据
        minuteenddate=self.__GetDeltaDate(t.strftime("%Y-%m-%d", t.localtime()),1)

        # 如果是15:30前，在现有库的最新日期前增加一天日期开始算起
        # 如果是15:30后，以当日计算
        # if Util.IsAfterBell()==False:
        #     minuteenddate=self.__GetDeltaDate(minuteenddate,-1)

        if minutestartdate==None:
            minutestartdate=self.defaultMinuteStartDate
        else:
            # 返回格式是2020-07-23 09:31:00,所以要取前10位
            minutestartdate=self.__GetExistingEndDate(index,'m')[:10]

            # 在现有库的日期前增加一天日期
            minutestartdate=self.__GetDeltaDate(minutestartdate,1)
            
            # minutestartdate=datetime.datetime.strptime(minutestartdate,'%Y-%m-%d')
            # offset = datetime.timedelta(1)
            # minutestartdate=(minutestartdate + offset).strftime('%Y-%m-%d')

        # self.FetchMinuteBar2CSV(index,minutestartdate,enddate)
        self.FetchBar2CSV(index, minutestartdate,minuteenddate,BarType='m')


    # 获取当前Index文件中的最后日期
    def __GetExistingEndDate(self,IndexID,BarType):

        if BarType=='d':
            DataFilePathName=os.path.join(self.DayBarPath,IndexID+'.csv')
        elif BarType=='m':
            DataFilePathName=os.path.join(self.MinuteBarPath,IndexID+'.csv')
        elif BarType=='m10':
            DataFilePathName=os.path.join(self.Minute10BarPath,IndexID+'.csv')

        # print('DataFilePathName:' + DataFilePathName)
        # 判断文件是否存在，如果文件不存在，返回默认开始日期，创建新文件
        if not os.path.exists(DataFilePathName):
            # f=open(DataFilePathName,"w+")
            # f.close()
            return None
        # 如果文件存在，返回最后一天的日期
        else:
            with open(DataFilePathName,encoding='UTF-8') as file_obj:
                AllLines = file_obj.readlines()
                # print(len(AllLines))
                # 获取最后一行的第一个字段， 即最后日期
                if len(AllLines)>1:
                    targetLine = AllLines[-1]
                    LastDayDate=targetLine.split(',')[0]
                    # print(LastDayDate)
                    return LastDayDate
                else:
                    return None

    # 获取Index List dataframe()
    def __GetIndexList(self):
        tmp_lst=[]
        with open(self.IndexListCSVPathName,encoding='UTF-8') as file_obj:
            
            reader = csv.reader(file_obj)

            for row in reader:
                tmp_lst.append(row)
        
        # self.dfIndex= pd.DataFrame(tmp_lst[1:], columns=tmp_lst[0]) 
        self.dfIndex= pd.DataFrame(tmp_lst[1:], columns=tmp_lst[0])
        print(self.dfIndex)

    # 抓取保存日线、分钟线、10分钟线数据，将之前的FetchDayBar2CSV、FetchMinuteBar2CSV合并
    # 抓取保存日线数据
    def FetchBar2CSV(self, IndexID, startdate,enddate,BarType='d'):

        # 如果是今日15:30前，在现有库的最新日期前增加一天日期开始算起
        # 如果是15:30后，以当日计算

        if startdate==Util.GetTodayDateString() and self.bIsAfterBell==False:
            print(IndexID,':今日数据未产生')
        else:

            if self.bIsAfterBell==False:
                enddate=self.__GetDeltaDate(enddate,-1)

            if BarType=='d':
                DataFilePathName=os.path.join(self.DayBarPath,IndexID +'.csv')

                df=JQDataFeeder().GetDayPriceBarbySE(IndexID,startdate,enddate)
            
                df.index.name = 'date'

            elif BarType=='m':
                DataFilePathName=os.path.join(self.MinuteBarPath,IndexID +'.csv')

                df=JQDataFeeder().GetMinutePriceBarbySE(IndexID,startdate,enddate)
            
                df.index.name = 'datetime'
            
            elif BarType=='m10':
                DataFilePathName=os.path.join(self.Minute10BarPath,IndexID +'.csv')

                df=JQDataFeeder().GetMinute10PriceBarbySE(IndexID,startdate,enddate)
            
                df.index.name = 'datetime'

            # print(df)
            # 删除不含数据的日期、时间
            nan_value = float("NaN")
            df.replace("", nan_value, inplace=True)
            df.dropna(subset = ["open"], inplace=True)

            if not os.path.exists(DataFilePathName):
                df.to_csv(DataFilePathName, mode='a',sep=',', header=True, index=True)
            else:
                df.to_csv(DataFilePathName, mode='a',sep=',', header=False, index=True)
            
            print('Done:' + IndexID + ':' +str(len(df)))
        # print('\n')
    
    # 从JQData获取交易日期
    # 根据当前时间判断是否要新加入
    def __RunTradingDaysMaintenance(self):

        startdate='2005-01-01'

        # enddate=t.strftime("%Y-%m-%d", t.localtime()) 
        enddate='2020-12-31'

        ExistingEndDate=self.__GetTradingDaysExistingEndDate()

        newstardate=self.__GetDeltaDate(ExistingEndDate,1)
        
        if ExistingEndDate!=None:
            ndarray=JQDataFeeder().GetTradingDays(newstardate,enddate)
        else:
            ndarray=JQDataFeeder().GetTradingDays(startdate,enddate)
        
        df = pd.DataFrame(ndarray)
        print(df)
        # print(df.shape)
        # df.drop(0,axis=1)
        # print(df)

        if not os.path.exists(self.TradingDaysPathName):
            df.to_csv(self.TradingDaysPathName, mode='a',sep=',', header=False, index=False)
        else:
            df.to_csv(self.TradingDaysPathName, mode='a',sep=',', header=False, index=False)

    # 获取当前Index文件中的最后日期
    def __GetTradingDaysExistingEndDate(self):

        # 判断文件是否存在，如果文件不存在，返回None
        if not os.path.exists(self.TradingDaysPathName):
            return None

        # 如果文件存在，返回最后一天的日期
        else:
            with open(self.TradingDaysPathName,encoding='UTF-8') as file_obj:
                AllLines = file_obj.readlines()
                # print(len(AllLines))
                # 获取最后一行的第一个字段， 即最后日期
                if len(AllLines)>1:
                    targetLine = AllLines[-1]
                    LastDayDate=targetLine[:10]
                    # print(LastDayDate)
                    return LastDayDate
                else:
                    return None

if __name__=='__main__':
    # 执行时间：
    begin = datetime.datetime.now()

    DataMaintain().RunMaintain()
    # DataMaintain()._DataMaintain__RunTradingDaysMaintenance()
    end = datetime.datetime.now()
    print('DataMaintain().RunMaintain()运行时间：' + str(end-begin))

    

# DataMaintain().__GetIndexList()




