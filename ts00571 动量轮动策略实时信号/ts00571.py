
import config

# 微信消息接口及其它公共模块接口
import sys
sys.path.append('C:\\Users\\Aaron\\Documents\\MyMobileBooks_800_Reading\\MyTSSnippets\\CommonModules')
sys.path.append('C:\\Users\\Aaron\\Documents\\MyMobileBooks_800_Reading\\MyTSSnippets\\CommonModules\\WeChatAPIWrapper')

from DataFeeder import *
from DataMaintain import DataMaintain
from WeChatAPIWrapper import WeChatAPIWrapper

from Util import *

# import Util #as Util

from Strategy import *

from Account import *

from Trading import *

from Optimizer import *

import pandas as pd
import tushare as ts
import talib
import time
from matplotlib import pyplot as plt
import datetime
import numpy as np
from dateutil.relativedelta import relativedelta

import os
import smtplib  #用于发送邮件
from email.mime.text import MIMEText
from email.header import Header

from twilio.rest import Client
from requests.adapters import HTTPAdapter

import time
import logging
from queue import Queue
import threading

# 为一些数据类提供更直接的表示，如Benchmark、Account、
from dataclasses import dataclass

# 用于寻找某些特征的文件
import glob

import csv


# 单次交互查询模式

def RunInteractiveMode():
    
    while(1):

        # if Util.IsTradingDays(Util.GetTodayDateString())==False :
        #     print('非交易日')
        #     exit()

        # if Util.IsAfterBell():
        #     print('已收盘')
        #     exit()

        # if Util.IsBeforeBell():
        #     print('未开盘')
        #     time.sleep(10)
        #     continue

        lstStrategy=Util.GetStrategyIDList()
        
        for eachStrategy in lstStrategy:
            # 动态生成策略类
            dynStrategyClass=globals()['StrategyDL' + eachStrategy]
            st = dynStrategyClass()

            st.bPrintFlag=True
            
            print('==============' + st.cg_StrategyName + '============')

            if config.g_silentmode==False:
                print(st.ETFList)

            # 获取参数。默认值
            st.cg_VRDays=Util.GetVRDays(st.cg_VRDays)
            st.cg_AVDays=Util.GetAVDays(st.cg_AVDays)
            
            # 获取当前日期和时间
            theDate=Util.GetDate() # '如2020-07-16'
            theTime=Util.GetTime() #'如13:05:00'

            # 程序执行时间：
            begin = datetime.datetime.now()
            st.GetTransactionSignal(theDate, theTime)

            # 打印策略各指数结果
            printDF=st.dfOutput
            printDF.iloc[:,2]=printDF.iloc[:,2].apply(Util.Float2Percent)
            printDF.iloc[:,3]=printDF.iloc[:,3].apply(Util.Float2Percent)
            # printDF['']
            print(printDF)

            end = datetime.datetime.now()
            print('GetTransactionSignal运行时间：' + str(end-begin))

            # 显示该策略此次Summary，如某ETF 涨幅等信息


        IsContinue=input('是否继续:q.退出；其它键.继续[继续]')

        if IsContinue=='q':
            exit()

    
    input()

# 实时循环监控模式
# 需要Account类、
def RunRealTimeMode(lstStrategy):

    # 实时监控类
    rt=Trading_RealTime()

    # 程序执行时间：
    begin = datetime.datetime.now()
    rt.Run(lstStrategy)
    #
    end = datetime.datetime.now()
    print('程序运行时间：' + str(end-begin))

# 回测模式  
# 输入：起始、结束日期，
# 输出：回测结果，收益率、最大回撤；显示benchmark的收益率              
def RunBackTestMode(lstStrategyID):
    # 指定起始、结束日期
    
    # startdate=Util.GetDate()

    # 默认结束日期为当天日期，开始日期为之前20天

    # 如果是当日收盘前，按前一天的数据，如果是当日收盘后，按当日数据回测（不过还得做成看数据库最后一天日期）
    
    if config.g_DefaultEndDate=='':
        defaultenddate=Util.GetTodayDateString()

        if Util.IsAfterBell()==False:
            defaultenddate=Util.DateDelta(defaultenddate,-1)
    else:
        defaultenddate=config.g_DefaultEndDate

    defaulstartdate=Util.DateDelta(defaultenddate,-30)
    defaulstartdate=config.g_DefaultStartDate

    startdate=Util.GetCustomizedDays('开始日期',defaulstartdate)
    # enddate=Util.GetDate()

    enddate=Util.GetCustomizedDays('结束日期',defaultenddate)

    Runtime=Util.GetCustomizedDays('交易时间','14:30:00')

    strategyIDList=Util.GetStrategyIDList()

    # 获取最符合的开始和结束日期
    startdate=Util.GetCloseAfterTradingDate(startdate)
    # print(startdate)
    # print(type(startdate))
    enddate=Util.GetCloseBeforeTradingDate(enddate)

    bt=Trading_BackTest(startdate,enddate)

    while(1):

        for eachStrategyID in strategyIDList:
            # 执行时间：
            begin = datetime.datetime.now()

            bt.Run(eachStrategyID,Runtime)

            end = datetime.datetime.now()
            print('bt.Run(eachStrategyID)程序运行时间：' + str(end-begin))
    
    
# 寻优模式  
# 输入：起始、结束日期，
# 输出：回测结果，收益率、最大回撤；显示benchmark的收益率   

def RunOptimizeMode(lstStrategy):

    # defaultenddate=Util.GetTodayDateString()

    if config.g_DefaultEndDate=='':
        defaultenddate=Util.GetTodayDateString()

        if Util.IsAfterBell()==False:
            defaultenddate=Util.DateDelta(defaultenddate,-1)
    else:
        defaultenddate=config.g_DefaultEndDate

    if Util.IsAfterBell()==False:
        defaultenddate=Util.DateDelta(defaultenddate,-1)

    defaulstartdate=Util.DateDelta(defaultenddate,-30)
    defaulstartdate=config.g_DefaultStartDate

    startdate=Util.GetCustomizedDays('开始日期',defaulstartdate)
    # enddate=Util.GetDate()

    enddate=Util.GetCustomizedDays('结束日期',defaultenddate)

    opt=Optimizer(startdate,enddate)

    # 执行时间：
    begin = datetime.datetime.now()
    while(1):

        theStrategyID=str(input('输入策略ID号：010.中国宽基;020.环球宽基;030.行业ETF；[010]'))

        if theStrategyID=='' or theStrategyID=='010':
            theStrategyID='010'
        
        opt.StrategyID=theStrategyID

        opt.GetBestParameters()

        end = datetime.datetime.now()
        print('opt.GetBestParameters()程序运行时间：' + str(end-begin))
        
        IsContinue=input('是否继续:q.退出；其它键.继续[继续]')

        if IsContinue=='q':
            exit()

# 主程序的初始化，各个全局参数的设置
def MainInit():
    

    # JQDataFeeder
    config.g_JQDataFeeder=JQDataFeeder()
    
     # TSDataFeeder
    config.g_TSDataFeeder=TSDataFeeder()

    # g_DataFeeder=LocalDataFeeder()
    config.g_DataFeeder=LocalDataFeederMemory() #调用内存数据加快速度

    
    # if g_WechatSwitchOn==True:
    #     g_wechat=WeChatAPIWrapper.WeChatAPIWrapper()
    #     # g_wechat.SendMessage()
    #     g_wechat.Start()
        
    #     CurrentDateTime=Util.GetLongDateTime()
    #     g_wechat.SendWeChatMessage(CurrentDateTime + ': ts00571 starting...')
 

    # 建立ETFList NamedTuple，便于程序中直接引用，而不用每次都从JQData调用，节省时间
    # 还是在LocalDataFeeder中实现
    # global g_dicETFList

    # LocalDB=LocalDataFeeder()
    # g_dicETFList=LocalDB.GetETFList()

if __name__ == "__main__":
    
    # 运行模式选择：
    # 1. 单次交互模式：查询各个策略当时的信号状态
    # 2. 实时监控模式：每隔5分钟查询一次数据，判断并发送信号
    # 3. 回测模式：选择某个或全部的策略，进行某段时间的回测并显示结果

    lstStrategy=['010','020','030']
    # lstStrategy=['030']

    
    config.g_SelectedMode=str(input('模式选择-1. 单次交互模式；2. 实时监控模式;3. 回测模式;4. 优化模式[1]:'))

    if config.g_SelectedMode=='':
        config.g_SelectedMode='1'

    

    ############交互模式####################
    if config.g_SelectedMode=='1':
        # g_WechatSwitchOn=False
        config.g_debugmode=True
        # g_silentmode=True
        config.g_silentmode=False
        
        # 初始化
        MainInit()
        
        RunInteractiveMode()

    ############实时监控模式####################
    elif config.g_SelectedMode=='2':
        # g_WechatSwitchOn=True
        config.g_WechatSwitchOn=False
        # g_silentmode=False
        config.g_silentmode=True
        config.g_debugmode=False

        # 初始化
        MainInit()

        RunRealTimeMode(lstStrategy)

    ############回测模式####################
    elif config.g_SelectedMode=='3':
        # g_WechatSwitchOn=False
        config.g_silentmode=True
        config.g_debugmode=False

        # 初始化
        MainInit()

        RunBackTestMode(lstStrategy)

    ############优化模式####################
    elif config.g_SelectedMode=='4':
        config.g_WechatSwitchOn=False
        config.g_silentmode=True

        # 初始化
        MainInit()
        RunOptimizeMode(lstStrategy)
    
input("Press Enter key to exit.")

