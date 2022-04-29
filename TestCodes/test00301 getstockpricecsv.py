


# 目的：
# 从tushare下载股票价格的CSV文件，分别存为未复权和前复权文件，后期可以再加入财报数据。
# 
# 目的是有一个本地数据库，能通过excel直接读取，在excel中进行一些数据的分析，比如骑行客之前的分析国庆。
# 长远看是能够为策略库做好准备，没有必要每次都要上网抓数据。
# 
# 代码是stocklist.csv，可能还会有将来其它的代码库，比如分析沪深300的、指数的。
# 
# 重要的一点是能够增量存取数据，能够识别数据中的开头、末尾分别是什么数据
# 
# 变量：
# stocklist的位置
# csv文件夹位置
# 开始日期
# 结束日期
# 
# 函数：
# *.解析code名称，转换为需要的格式，如000001.sz或者sh600001
# *.返回需要下载的代码清单 getcodelist
# *.从图share，返回dataframe
#     #获取未复权行情
#   pro = ts.pro_api()
#   df = pro.daily(ts_code='000001.SZ', start_date='20180701', end_date='20180718')
#   
#   #取000001的前复权行情
#  df = ts.pro_bar(ts_code='000001.SZ', adj='qfq', start_date='20180101', end_date='20181011'
# 
# 
# 要点：
# *. 多用函数，封装，便于编写分段思考、查错和将来的重用
# *.从tushare获取datafarme，这个函数最好做成一个通用接口，因为将来很可能要从不同途径获取数据
# *.dataframe保存为csv文件函数
# *.csv文件如何在前面插入行、如何在后面插入行
# *.pro_bar接受2019-11-01的形式，但是pro.daily不接受。
# *.结论是用pro_bar，而不用pro.daily
# *.如何从已有csv中或dataframe中找出开始日期和结束日期
# *.#获取已有文件的startdate、enddate，重新建立一个新dataframe，分别，然后写入旧dataframe
    #这里的逻辑：对数据进行组合，wrangling，全部组合在一起，然后一次性的排序再删除重复数据，即可
    #关键在于dataframe的操作

# coding: utf-8

import pandas as pd
import tushare as ts
import talib
from matplotlib import pyplot as plt
from datetime import datetime
import matplotlib
import csv
import os

#当前文件的路径
pwd = os.getcwd()
#当前文件的父路径
father_path=os.path.abspath(os.path.dirname(pwd)+os.path.sep+".")

stocklistwholepath=father_path + "/MyTSSnippets/DataRepository/db00021/stocklist1.csv"
csvfolderwholepath=father_path + "/MyTSSnippets/DataRepository/db00081/weekly/"
csvfolderwholepath_weekly=father_path + "/MyTSSnippets/DataRepository/db00081/weekly/"

# 用于 pro_bar函数
# startdate='2019-01-05' 
enddate = datetime.today() #开始时间结束时间，选取最近一年的数据
enddate = str(enddate)[0:10]

# 用于weekly等函数
startdate='20190101' #用于weekly等函数
enddate='20191203'

token='f20927201ecc20e3cea9279abacfbb1d39a9624820d9b2f94613f722'
# global pro
pro=ts.pro_api(token)

def ParseCode(CodeName):
    #增加SH/SZ等后缀，如000001.sz
    if CodeName[0]=='0' or CodeName[0]=='3':
        return CodeName + '.SZ'
    elif CodeName[0]=='6':
        return CodeName + '.SH'
    # return ParsedCodeName

def ParseCodeFileName(CodeName):
    #增加SH/SZ等后缀，如SH600001
    if CodeName[0]=='0' or CodeName[0]=='3':
        return 'sz' + CodeName
    elif CodeName[0]=='6':
        return 'sh' + CodeName  

def getcodelist():
    codelist=[]
    with open(stocklistwholepath,newline='', encoding='"utf-8-sig') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        for row in csv_reader:
            # print(row['code'],row['name'])
            codelist.append(row['code'])
    return codelist

def getstockdataframe(channel, code,startdate, enddate, freq='d'):
    #转换为sz或sh开头格式
    parsedcodename=ParseCode(code)

    if channel=='tushare':
#          df = pro.daily(ts_code='000001.SZ', start_date='20180701', end_date='20180718')
        if freq=='d':
            df = ts.pro_bar(ts_code=parsedcodename, adj='None', start_date=startdate, end_date=enddate) 
        elif freq=='w':
            df = pro.weekly(ts_code=parsedcodename, start_date=startdate, end_date=enddate, fields='ts_code,trade_date,open,high,low,close,vol,amount')
        # df = pro.daily(ts_code=codename, start_date=startdate, end_date=enddate)
        # df = pro.daily(ts_code=codename, start_date='20190701', end_date='20191122')
        # df = pro.daily(ts_code='000001.SZ', start_date='20180701', end_date='20180718')
        # print(df.head)
        return df


def savecsv(code,df,freq):
    #判断文件是否存在，如何存在，则判断数据的前后日期，如果不存在，则创建新文件，进行读写
    if freq=='d':
        filename=csvfolderwholepath + ParseCodeFileName(code)
    elif freq=='w':
        filename=csvfolderwholepath_weekly + ParseCodeFileName(code)
    
    if os.path.exists(filename):
        appenddataframe(df, filename)
    else:
        df.to_csv(filename + '.csv')
    
def appenddataframe(newdataframe, filename):
    #获取已有文件的startdate、enddate，重新建立一个新dataframe，分别，然后写入旧dataframe
    #这里的逻辑：对数据进行组合，wrangling，全部组合在一起，然后一次性的排序再删除重复数据，即可
    #关键在于dataframe的操作
    return 0


if __name__=="__main__":
    codelist=getcodelist()
    
    # codelist=['000157']
    
    for code in codelist:
        #第一版这里的逻辑有问题，应该是先找到本地数据库中的开始日期和结束日期，
        #如果本地数据库数据容量小于待查数据，则进行tushare抓取，
        # 并且只找不存在的日期数据（小于开始日期的、晚于结束日期的）
        # 但必须默认已有数据是连续的，中间不存在空档数据
        # 否则不应该抓取，更不用说数据多余待查日期的数据

        df=getstockdataframe('tushare', code,startdate, enddate,freq='w')
        # print(df.head)
        savecsv(code, df,freq='w')