
from jqdatasdk import *
import datetime
import abc
from abc import ABC, abstractmethod
import pandas as pd
import numpy as np
import os

import config

# 数据来源的通用类
# class DataFeeder(metaclass=abc.ABCMeta):
class DataFeeder(ABC):
    def __init__(self):
        # theDataFeed=
        pass
    
    def GetCount(self):
       print('Father Class')

    def SetChildClass(self,ChildClassName):
        raise NotImplementedError

    #获取实时价格
    # @staticmethod
    @abc.abstractmethod
    def GetPriceDFofTheTime(self,index,thedatetime,IncludeNow=True):
        raise NotImplementedError

    # 获取某几日的日线收盘价格，格式为date,close
    # @staticmethod
    @abc.abstractmethod
    def GetDayPriceBar(self,index,days,enddate,IncludeNow=False):
        
        raise NotImplementedError
    
    # 获取某个时间段的close价格数据
    # @staticmethod
    @abc.abstractmethod
    def GetTheDateTimePrice(self,index,thedate,thetime):
        
        raise NotImplementedError

    # @staticmethod
    @abc.abstractmethod
    def GetTradingDays(self,startdate,enddate):
        pass

    # @staticmethod
    @abc.abstractmethod
    def GetSecurityName(self,Index):
        pass


# JoinQuant的数据接口类
class JQDataFeeder(DataFeeder):
    def __init__(self):

        # auth('13651829783','aaronjoinquant')
        auth('18136078552','078552')

    # JQData专有
    def GetCount(self):
        
        count=get_query_count()
        return count

    # 获取股票代码和名称清单
    def GetCodeList(self,type,date=''):
        return get_all_securities(type,date)

    #获取实时价格
    
    # 通用函数，可以通过本地函数来代替
    def GetPriceDFofTheTime(self,index,thedatetime,IncludeNow=True):
        df=get_bars(index,1,unit='1m', fields=['date','close'], include_now=IncludeNow, end_dt=thedatetime,fq_ref_date=datetime.date(2000, 1, 1),df=True) 
        return df

    # 获取分钟线收盘价格(通过起始、结束日期），格式为date,close
    def GetMinutePriceBarbySE(self,security,stardate,enddate):
        df=get_price(security, start_date=stardate, end_date=enddate, frequency='minute', fields=None, skip_paused=False, fq='pre', count=None, panel=True, fill_paused=True)
        return df

    # 获取10分钟线收盘价格(通过起始、结束日期），格式为date,close
    def GetMinute10PriceBarbySE(self,security,stardate,enddate):
        df=get_price(security, start_date=stardate, end_date=enddate, frequency='10m', fields=None, skip_paused=False, fq='pre', count=None, panel=True, fill_paused=True)
        return df

    # 获取某几日的日线收盘价格(通过起始、结束日期），格式为date,close
    def GetDayPriceBarbySE(self,security,stardate,enddate):
        df=get_price(security, start_date=stardate, end_date=enddate, frequency='daily', fields=None, skip_paused=False, fq='pre', count=None, panel=True, fill_paused=True)
        return df

    # 获取某几日的日线收盘价格，（通过前溯几天到结束日期），格式为date,close
    # @staticmethod
    # 通用函数，可以通过本地函数来代替
    def GetDayPriceBar(self,index,days,enddate,IncludeNow=False):
        
        df =get_bars(index, 
                         count=int(days), 
                         unit='1d',
                         fields=['date','close'],
                         include_now=IncludeNow,
                         end_dt=enddate)
        return df
    
    # 获取某个时间段的close价格数据
    # @staticmethod
    def GetTheDateTimePrice(self,index,thedate,thetime):
        
        thedatetime=thedate + ' ' + thetime
        
        thedatetime=datetime.datetime.strptime(thedatetime,"%Y-%m-%d %H:%M:%S")

        df_rt = self.GetPriceDFofTheTime(index,thedatetime)
      
        # print('GetTheDateTimePrice' + str(df_rt['close']))
        return df_rt['close'][0]

    # @staticmethod
    def GetTradingDays(self,startdate,enddate):
        return get_trade_days(start_date=startdate, end_date=enddate, count=None)

    
    def GetSecurityName(self,Index):
        return get_security_info(Index).display_name



# Tushare的数据接口类，用于取代JQData的免费接口
class TSDataFeeder(DataFeeder):
    def __init__(self):

        # auth('13651829783','aaronjoinquant')
        pass

    # # JQData专有
    # def GetCount(self):
        
    #     count=get_query_count()
    #     return count

    # 获取股票代码和名称清单
    def GetCodeList(self,type,date=''):
        return get_all_securities(type,date)

    #获取实时价格
    
    # 通用函数，可以通过本地函数来代替
    def GetPriceDFofTheTime(self,index,thedatetime,IncludeNow=True):
        df=get_bars(index,1,unit='1m', fields=['date','close'], include_now=IncludeNow, end_dt=thedatetime,fq_ref_date=datetime.date(2000, 1, 1),df=True) 
        return df

    # 获取分钟线收盘价格(通过起始、结束日期），格式为date,close
    def GetMinutePriceBarbySE(self,security,stardate,enddate):
        df=get_price(security, start_date=stardate, end_date=enddate, frequency='minute', fields=None, skip_paused=False, fq='pre', count=None, panel=True, fill_paused=True)
        return df

    # 获取10分钟线收盘价格(通过起始、结束日期），格式为date,close
    def GetMinute10PriceBarbySE(self,security,stardate,enddate):
        df=get_price(security, start_date=stardate, end_date=enddate, frequency='10m', fields=None, skip_paused=False, fq='pre', count=None, panel=True, fill_paused=True)
        return df

    # 获取某几日的日线收盘价格(通过起始、结束日期），格式为date,close
    def GetDayPriceBarbySE(self,security,stardate,enddate):
        df=get_price(security, start_date=stardate, end_date=enddate, frequency='daily', fields=None, skip_paused=False, fq='pre', count=None, panel=True, fill_paused=True)
        return df

    # 获取某几日的日线收盘价格，（通过前溯几天到结束日期），格式为date,close
    # @staticmethod
    # 通用函数，可以通过本地函数来代替
    def GetDayPriceBar(self,index,days,enddate,IncludeNow=False):
        
        df =get_bars(index, 
                         count=int(days), 
                         unit='1d',
                         fields=['date','close'],
                         include_now=IncludeNow,
                         end_dt=enddate)
        return df
    
    # 获取某个时间段的close价格数据
    # @staticmethod
    def GetTheDateTimePrice(self,index,thedate,thetime):
        
        thedatetime=thedate + ' ' + thetime
        
        thedatetime=datetime.datetime.strptime(thedatetime,"%Y-%m-%d %H:%M:%S")

        df_rt = self.GetPriceDFofTheTime(index,thedatetime)
      
        # print('GetTheDateTimePrice' + str(df_rt['close']))
        return df_rt['close'][0]

    # @staticmethod
    def GetTradingDays(self,startdate,enddate):
        return get_trade_days(start_date=startdate, end_date=enddate, count=None)

    
    def GetSecurityName(self,Index):
        return get_security_info(Index).display_name
    
# 本地数据，用于不需要每次都从网上抓取日线数据、分钟线数据
# ！！这里的重点在于：首先用一个通用的内部函数__GetDataFrame，然后用DataFrame的选择功能来找到需要的数据。
# 要把Date或者DateTime设为Index
# 然后用.loc()来选择
class LocalDataFeeder(DataFeeder):
    def __init__(self):
        self.LocalDataPath=''
        self.LocalDayBarPath = 'C:/Users/Aaron/Documents/MyMobileBooks_800_Reading/MyTSSnippets/DataRepository/db00071/Day'
        self.LocalMinuteBarPath ='C:/Users/Aaron/Documents/MyMobileBooks_800_Reading/MyTSSnippets/DataRepository/db00071/Minute'
        self.LocalMinute10BarPath ='C:/Users/Aaron/Documents/MyMobileBooks_800_Reading/MyTSSnippets/DataRepository/db00071/Minute10'
        self.ETFListPathName='C:/Users/aaron/Documents/MyMobileBooks_800_Reading/MyTSSnippets/ts00571 动量轮动策略实时信号/Data_Common/ETFList.csv'
        self.TradingDaysPathName="C:/Users/aaron/Documents/MyMobileBooks_800_Reading/MyTSSnippets/DataRepository/db00131/tradingdays.csv"
        # JQDataFeeder，用于包装实现本地数据无法实现的接口，还是用JQData实现
        self.theJQDataFeeder=JQDataFeeder()
        self.theTSDataFeeder=TSDataFeeder()

        self.dicETFList=self.GetETFList()

        # 开始就读出所有的历史分钟数据，而不是每次都要重新读一遍
        self.cg_dfHistoryDayData=pd.DataFrame()
        self.cg_dfHistoryMinuteData=pd.DataFrame()
        self.cg_dfHistoryMinute10Data=pd.DataFrame()

    # 抓取所有的该Index对应的历史数据，而不是到用的时候才抓很多遍
    # def InitIndexHistoryData(self,IndexID):
    #     self.cg_dfHistoryMinuteData=self.__GetDataFrame(IndexID,'m')
    #     self.cg_dfHistoryDayData=self.__GetDataFrame(IndexID,'d')

    # 检查输入enddate和当前csv中的日期是否有冲突，
    def __CheckInputEndDate(self, df_csv,enddate):

        # lastdateDFCSV=df_csv['datetime'][-1]
        print(df_csv.tail(1))
        lastdateDFCSV=df_csv.tail(1).iloc[0,0] # ['datetime']

        print('lastdateDFCSV:')
        print(lastdateDFCSV)
        
        # 当enddate超过库中最后一天时间时，取库中最后一天日期
        if datetime.datetime.strptime(enddate,'%Y-%m-%d')>=datetime.datetime.strptime(lastdateDFCSV,'%Y-%m-%d'):
            return lastdateDFCSV
        else:
            return enddate
        pass

    #获取实时价格
    # 通用函数，可以通过本地函数来代替
    # 如果是当日的实时，要调用JQData
    def GetPriceDFofTheTime(self,index,thedatetime,IncludeNow=True):
        
        # begin = datetime.datetime.now()
        
        df=self.__GetDataFrame(index,'m')
        # df=self.cg_dfHistoryMinuteData

        # end = datetime.datetime.now()
        # print('df=self.__GetDataFrame运行时间：' + str(end-begin))

        # print(df.loc[thedatetime].to_frame().T)
        # print(type(df.loc[thedatetime].to_frame().T))
        try:
            if df!=None:
                return df.loc[thedatetime].to_frame().T
        except:
            return self.theJQDataFeeder.GetPriceDFofTheTime(index,thedatetime)

    # 获取某几日的日线收盘价格(通过起始、结束日期），格式为date,close
    # 查错，当enddate超过库中最后一天时间时，取库中最后一天日期
    def GetMinutePriceBarbySE(self,security,stardate,enddate):
          
        df=self.__GetDataFrame(security,'m')
        # df=self.cg_dfHistoryMinuteData

        # print(df.tail(2))
        actualenddate=enddate 

        actualenddate=self.__CheckInputEndDate(df,enddate)

        print(actualenddate)
        # LastDateDF=df['date'][-1]
        
        # if enddate>=LastDateDF:
            # actualenddate=LastDateDF
            # return self.theJQDataFeeder.GetMinutePriceBarbySE(security,startdate,enddate)
        # else:
            # actualenddate=enddate
        # print(df.loc[stardate:enddate])
        # print(type(df.loc[stardate:enddate]))
        return df.loc[stardate:actualenddate]


    # 获取某几日的日线收盘价格(通过起始、结束日期），格式为date,close
    # 查错，当enddate超过库中最后一天时间时，取库中最后一天日期
    def GetDayPriceBarbySE(self,security,stardate,enddate):
          
        df=self.__GetDataFrame(security,'d')
        # df=self.cg_dfHistoryDayData
        # print(df.loc[stardate:enddate])
        return  df.loc[stardate:enddate]

    # 获取某几日的日线收盘价格，（通过前溯几天到结束日期），格式为date,close
    # 通用函数，可以通过本地函数来代替
    # 这里的IncludeNow要注意，在回测时要看到底是否要考虑
    # 要有查错，当最晚日期超过库中时间时，取最后的日期
    def GetDayPriceBar(self,index,days,enddate,IncludeNow=False):
    
        # 获取所有的日线数据
        df=self.__GetDataFrame(index,'d')
        # df=self.cg_dfHistoryDayData
        # print(df.loc[:enddate].tail(days))
        return df.loc[:enddate].tail(int(days))

        # print(type(df.index))
        # df['date'] = pd.to_datetime(df['date'],format='%y-%m-%d')
        # df['date'] = pd.to_datetime(df['date'])
        
        # df.set_index('date', inplace=True)

        # print(type(df.index))

        # print(df['2019-02'])
        # print(df['close'])

        # df.plot('date')
        # startdate=

        # df['date'] = pd.date_range('2020-1-1', periods=200, freq='d')

        # mask = (df['date'] > '2020-6-1') & (df['date'] <= enddate)

        # print(df.loc[mask])
        # =========================================
        # return df.loc[mask]
        # print(df.loc[:enddate])
        # print(df.date_range(enddate, periods=4, freq='D'))
        # print(df.loc[enddate].last('3D'))
        # print(df.loc[enddate].tail(3))
        
    
    # 获取某个时间段的close价格数据
    # @staticmethod
    def GetTheDateTimePrice(self,index,thedate,thetime):
        
        # 本地历史数据只有分钟线，如11:29:03要改为11:29:00
        
        thetime=thetime[:6] + '00'
        thedatetime=thedate + ' ' + thetime
        
        thedatetime=datetime.datetime.strptime(thedatetime,"%Y-%m-%d %H:%M:%S")

        # begin = datetime.datetime.now()
               
                
        df_rt = self.GetPriceDFofTheTime(index,thedatetime)

        # end = datetime.datetime.now()
        # print('df_rt = self.GetPriceDFofTheTime运行时间：' + str(end-begin))
    
        # print('GetTheDateTimePrice' + str(df_rt['close']))

        # 如果数据库中没有数据
        if df_rt.empty!=True:
            return df_rt['close'][0]
        else:
            print('from JQData：GetTheDateTimePrice')
            return self.theJQDataFeeder.GetTheDateTimePrice(index,thedate, thetime)

    # 返回Datatime格式List
    def GetTradingDays(self,startdate,enddate):

        print("def GetTradingDays")
        # print('From theJQDataFeeder')
        # print(self.theJQDataFeeder.GetTradingDays(startdate, enddate))
        # return self.theJQDataFeeder.GetTradingDays(startdate, enddate)
        df=pd.read_csv(self.TradingDaysPathName,names=['date'])
        # print(df.head(2))
        # df.index.name = 'date'
        
        df.set_index('date', inplace=True)
        # print(df.head(2))
        df=df[startdate:enddate]
        df=df.reset_index()
        df['date']=pd.to_datetime(df['date'],format="%Y-%m-%d")
        # df=df.astype(datetime)
        # print(df.head(2))

        # print(df)
        # lst=df['date'].flatten() #.tolist()
        lst=df['date'].tolist()
        # nparray=np.array(df)
        # lst=nparray.tolist()
        # lst=df.values.tolist() 
        # lst=df.tolist()    
        # df=df.set_index('IndexID').T.to_dict('list')
        # print(lst)
        return lst
    

    def GetSecurityName(self,Index):
        # print('From theJQDataFeeder')
        # return self.theJQDataFeeder.GetSecurityName(Index)
        return self.dicETFList[Index][0]
        # pass
    
    # 从数据获取所有ETF Index ID和Index Name的对应表，返回NamedTuple或Dict
    def GetETFList(self):
        df=pd.read_csv(self.ETFListPathName)
        df=df.set_index('IndexID').T.to_dict('list')
        # print(df)
        return df
    
    # 读取文件，获得一个Index所有数据的DataFrame
    def __GetDataFrame(self, IndexID,BarType='d'):
        if BarType=='d':
            LocalFilePathName=os.path.join(self.LocalDayBarPath,IndexID +'.csv')
        elif BarType=='m':
            LocalFilePathName=os.path.join(self.LocalMinuteBarPath,IndexID +'.csv')
        elif BarType=='m10':
            LocalFilePathName=os.path.join(self.LocalMinute10BarPath,IndexID +'.csv')

        df=pd.read_csv(LocalFilePathName)

        if BarType=='d':
            df['date'] = pd.to_datetime(df['date'])
            df.set_index('date', inplace=True)
        elif BarType=='m':
            df['datetime'] = pd.to_datetime(df['datetime'])
            df.set_index('datetime', inplace=True)
        elif BarType=='m10':
            df['datetime'] = pd.to_datetime(df['datetime'])
            df.set_index('datetime', inplace=True)

        # print(df)
        return df

# 目的：创建2个动态表(分钟线数据、日线数据)，包含多个数据程序运行时读入内容，加快读取速度，不用每次__GetDataFrame()
class LocalDataFeederMemory(LocalDataFeeder):

    def __init__(self):

        super(LocalDataFeederMemory, self).__init__()

        # 开始就读出所有的历史分钟数据，而不是每次都要重新读一遍
        

        # 用字典数据，如{'000300.XSHG', dataframe;...}
        self.cg_dicDFHistoryDayData={}
        self.cg_dicDFHistoryMinuteData={}
        self.cg_dicDFHistoryMinute10Data={}

        # 创建对象时将所有ETF的数据调入数据库
        self.__BuildIndexDataFrames()


    def __BuildIndexDataFrames(self):
        
        for eachETF in self.dicETFList:
            df1=self._LocalDataFeeder__GetDataFrame(eachETF,'d')
            self.cg_dicDFHistoryDayData[eachETF]=df1
            
            df2=self._LocalDataFeeder__GetDataFrame(eachETF,'m')
            self.cg_dicDFHistoryMinuteData[eachETF]=df2

            df3=self._LocalDataFeeder__GetDataFrame(eachETF,'m10')
            self.cg_dicDFHistoryMinute10Data[eachETF]=df3


    #获取实时价格
    # 通用函数，可以通过本地函数来代替
    # 如果是当日的实时，要调用JQData
    def GetPriceDFofTheTime(self,index,thedatetime,IncludeNow=True):
        
        df=pd.DataFrame()
        df=self.cg_dicDFHistoryMinuteData[index]

        try:
        
            if df.empty!=True:
                return df.loc[thedatetime].to_frame().T
        except:
            print('from JQData：GetPriceDFofTheTime')
            return self.theJQDataFeeder.GetPriceDFofTheTime(index,thedatetime)
    
    #获取实时价格
    # 通用函数，可以通过本地函数来代替
    # 如果是当日的实时，要调用JQData
    def GetPriceDFofTheTimeMinute10(self,index,thedatetime,IncludeNow=True):
        
        df=pd.DataFrame()
        df=self.cg_dicDFHistoryMinute10Data[index]
        # print(df)

        try:
        
            if df.empty!=True:
                # print(df.loc[thedatetime])
                return df.loc[thedatetime].to_frame().T
        except:
            # print(Exception)
            print('from JQData：GetPriceDFofTheTimeMinute10')
            return self.theJQDataFeeder.GetPriceDFofTheTime(index,thedatetime)


    # 获取某几日的日线收盘价格(通过起始、结束日期），格式为date,close
    # 查错，当enddate超过库中最后一天时间时，取库中最后一天日期
    def GetMinutePriceBarbySE(self,security,stardate,enddate):
          
        df=self.cg_dicDFHistoryMinuteData[security]

        actualenddate=enddate 

        actualenddate=self.__CheckInputEndDate(df,enddate)

        print(actualenddate)
        
        return df.loc[stardate:actualenddate]
    
    # 获取某几日的日线收盘价格(通过起始、结束日期），格式为date,close
    # 查错，当enddate超过库中最后一天时间时，取库中最后一天日期
    def GetMinute10PriceBarbySE(self,security,stardate,enddate):
          
        df=self.cg_dicDFHistoryMinute10Data[security]

        actualenddate=enddate 

        actualenddate=self.__CheckInputEndDate(df,enddate)

        print(actualenddate)
        
        return df.loc[stardate:actualenddate]


    # 获取某几日的日线收盘价格(通过起始、结束日期），格式为date,close
    # 查错，当enddate超过库中最后一天时间时，取库中最后一天日期
    def GetDayPriceBarbySE(self,security,stardate,enddate):
          
        # df=self.__GetDataFrame(security,'d')

        df=self.cg_dicDFHistoryDayData[security]
       
        return  df.loc[stardate:enddate]

    # 获取某几日的日线收盘价格，（通过前溯几天到结束日期），格式为date,close
    # 通用函数，可以通过本地函数来代替
    # 这里的IncludeNow要注意，在回测时要看到底是否要考虑
    # 要有查错，当最晚日期超过库中时间时，取最后的日期
    def GetDayPriceBar(self,index,days,enddate,IncludeNow=False):
    
        df=self.cg_dicDFHistoryDayData[index]
        
        return df.loc[:enddate].tail(int(days))

        
    
    # 获取某个时间段的close价格数据
    # @staticmethod
    def GetTheDateTimePrice(self,index,thedate,thetime):
        
        # 本地历史数据只有分钟线，如11:29:03要改为11:29:00
        
        thetime=thetime[:6] + '00'
        thedatetime=thedate + ' ' + thetime
        
        thedatetime=datetime.datetime.strptime(thedatetime,"%Y-%m-%d %H:%M:%S")

        # begin = datetime.datetime.now()
               
                
        df_rt = self.GetPriceDFofTheTime(index,thedatetime)

        # end = datetime.datetime.now()
        # print('df_rt = self.GetPriceDFofTheTime运行时间：' + str(end-begin))
    

        # 如果数据库中没有数据
        if df_rt.empty!=True:
            return df_rt['close'][0]
        else:
            print('from JQData GetTheDateTimePrice')
            return self.theJQDataFeeder.GetTheDateTimePrice(index,thedate, thetime)
    
    # 获取某个时间段的close价格数据
    # @staticmethod
    def GetTheDateTimeMinute10Price(self,index,thedate,thetime):
        
        # 本地历史数据只有分钟线，如11:29:03要改为11:29:00
        
        thetime=thetime[:6] + '00'
        thedatetime=thedate + ' ' + thetime
        
        thedatetime=datetime.datetime.strptime(thedatetime,"%Y-%m-%d %H:%M:%S")

        # begin = datetime.datetime.now()
               
                
        df_rt = self.GetPriceDFofTheTimeMinute10(index,thedatetime)

        # end = datetime.datetime.now()
        # print('df_rt = self.GetPriceDFofTheTime运行时间：' + str(end-begin))
    

        # 如果数据库中没有数据
        if df_rt.empty!=True:
            return df_rt['close'][0]
        else:
            print('from JQData GetTheDateTimeMinute10Price')
            return self.theJQDataFeeder.GetTheDateTimePrice(index,thedate, thetime)
 

if __name__=='__main__':
    # JQ=DataFeeder()

    # LocalDB=LocalDataFeeder()
    # ldfm=LocalDataFeeder()
    ldfm=LocalDataFeederMemory()


    begin = datetime.datetime.now()
    print(ldfm.GetPriceDFofTheTimeMinute10('000300.XSHG','2019-07-30 15:00:00'))
    end = datetime.datetime.now()
    print('ldfm.GetPriceDFofTheTime：' + str(end-begin))

    # ldfm.__BuildIndexDataFramesBuildIndexDataFrames()


    # tradingdays=LocalDB.GetTradingDays('2020-07-01','2020-07-23')
    # print(tradingdays)
    # dict=LocalDB.GetETFList()
    # print(dict['000300.XSHG'][0]) 

    # LocalDB.GetDataFrame('512800.XSHG','m')

    # LocalDB.GetDayPriceBar('512800.XSHG',10,'2020-07-25')

    # LocalDB.GetDayPriceBarbySE('512800.XSHG','2020-07-13','2020-07-25')

    # LocalDB.GetMinutePriceBarbySE('512800.XSHG','2020-07-23','2020-07-25')

    # print(LocalDB.GetPriceDFofTheTime('512800.XSHG','2020-01-3 09:31:00')['close'])

    # JQ.GetCount()