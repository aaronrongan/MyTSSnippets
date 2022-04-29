
from jqdatasdk import *
import datetime
import time


# 数据接口类
class JQDataInterface():
    def __init__(self):
        # 2020-7 新增账号
        # auth('13651829783','aaronjoinquant')
        
        # 2021-10-27 新增账号
        auth('18136078552','078552')

    @staticmethod
    def GetCount(self):
        
        count=get_query_count()
        return count

    #获取实时价格
    @staticmethod
    def GetPriceDFofTheTime(index,thedatetime,IncludeNow=True):
        
        df=get_bars(index,1,unit='1m', fields=['date','close'], include_now=IncludeNow, end_dt=thedatetime,fq_ref_date=datetime.date(2000, 1, 1),df=True) 
        return df

    # 获取某几日的日线收盘价格，格式为date,close
    @staticmethod
    def GetDayPriceBar(index,days,enddate,IncludeNow=False):
        
        df =get_bars(index, 
                         count=int(days), 
                         unit='1d',
                         fields=['date','close'],
                         include_now=IncludeNow,
                         end_dt=enddate)
        return df
    
    # 获取某个时间段的close价格数据
    @staticmethod
    def GetTheDateTimePrice(index,thedate,thetime):
        
        thedatetime=thedate + ' ' + thetime
        print(thedatetime)
        
        thedatetime=datetime.datetime.strptime(thedatetime,"%Y-%m-%d %H:%M:%S")

        df_rt = JQDataInterface.GetPriceDFofTheTime(index,thedatetime)
      
        # print('GetTheDateTimePrice' + str(df_rt['close']))
        return df_rt['close'][0]

    @staticmethod
    def GetTradingDays(startdate,enddate):
        return get_trade_days(start_date=startdate, end_date=enddate, count=None)

    @staticmethod
    def GetSecurityName(Index):
        return get_security_info(Index).display_name
        