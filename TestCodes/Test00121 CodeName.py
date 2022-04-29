# -*- coding: utf-8 -*-

#测试如何得到code对应的股票名称，在csv中

import csv
import os

#codelist=[]

with open(os.getcwd() + "/DataRepository/db00011.csv",newline='', encoding='UTF-8') as csv_file:
# with open('StockList.csv',newline='', encoding = 'UTF-8') as csv_file:

    csv_reader = csv.DictReader(csv_file) #,fieldnames=['symbol','name']
    dictcode={}
    dictname={}
    for row in csv_reader:
        dictcode[row['symbol']]=row['name']
        dictname[row['name']]=row['symbol']
    print(dictcode['000001'])
    print(dictname['光环新网'])
    # 转为列表，列表中多维字典
    # print(codelist)
    # csvlist1 = list(csv_reader)
    # print(csvlist1.count(1))
    # 将A当做为索引
    # csvlist2 = [row['code'] for row in csvlist1]
    # n = csvlist2.index('code')
    #根据下标值获取对应的字典n
    # csvlist3 = csvlist1[n]
    # print(csvlist2.index('002271'))
    # print(csvlist3['code'])
    # print(codelist.index('300383'))
    # csvlist3 = csvlist1[codelist.index('300383')]
    # print(csvlist3)
    # namevalue=codelist[2]['name']
    # print(namevalue)
    # n=csvlist2.index('300383')
    # print(n)
    # csvlist3=csvlist1[n]
    # BValue=csvlist3['300383']
    # print(BValue)