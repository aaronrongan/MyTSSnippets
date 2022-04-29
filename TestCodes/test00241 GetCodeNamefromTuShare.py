
#从Tushare中获取代码名称,数据类型 pandas.core.frame.DataFrame
#将结果导入CSV，后面就可以通过test012来实现
# #-*- coding: utf-8 -*- 如果不写可能会乱码

import tushare as ts
import pandas as pd
import os
# import pandas.DataFrame as pdf
import csv

token='f20927201ecc20e3cea9279abacfbb1d39a9624820d9b2f94613f722'

def Save2CSV():
    pro=ts.pro_api(token)
    df = pro.stock_basic(exchange='', list_status='L', fields='ts_code,symbol,name,area,industry,list_date')
    df.to_csv(os.getcwd() + "/DataRepository/db00011.csv", encoding="utf-8-sig", header=True, index=False)

# print(data)
def GetCodebyName(Name):
    return 0

def GetNamebyCode(code):
    return 0

Save2CSV()
