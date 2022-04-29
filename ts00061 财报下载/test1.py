
# 目的：建立财报下载器，从新浪财经获取PDF

# 参考文献：IRF19091503 财务报表下载器项目

# 网址： https://www.lixinger.com/analytics/company/sz/300383/detail/announcement?announcement-type=fs&page-index=0

# To Do List:
# 1. 增加下载路径识别，如果不存在，提示创建
# 2. 不同电脑下载的不同路径如何区分
# 3. 根据不同电脑下载到不同的文件夹
# 4. 用selenium从Lixinger下载更全格式的财报

#191026 更新
#使用命令行独立执行方式，用户输入年份、代码，已有的重复文件不要覆盖, 打包成一个独立文件ts0061

# 191128
# 已转移到snippets目录。Github目录停止更新。

#要点：
#notepad++改CSV为UTF-8-BOM
#使用如下格式：注意用UTF-8-SIG
# #with open('./StockList.csv', newline='', encoding = 'UTF-8-sig') as csv_file:


import csv
import os
# from DwnFR_Sina import DownloadFR

import re
import requests
from bs4 import BeautifulSoup
import lxml
import urllib
import os
import csv
import socket

import sys


#####定义全局变量
#下载地址
#文件命名规则
#错误提示

#下载地址
url_ar_sample='http://vip.stock.finance.sina.com.cn/corp/go.php/vCB_Bulletin/stockid/002271/page_type/ndbg.phtml'
global url_ar_1,url_ar_2
url_ar_1='http://vip.stock.finance.sina.com.cn/corp/go.php/vCB_Bulletin/stockid/'
url_ar_2='/page_type/ndbg.phtml'

global url_q1_1
url_q1='http://vip.stock.finance.sina.com.cn/corp/go.php/vCB_BulletinYi/stockid/002271/page_type/yjdbg.phtml'
url_q1_1='http://vip.stock.finance.sina.com.cn/corp/go.php/vCB_Bulletin/stockid/'
url_q1_2='/page_type/yjdbg.phtml'

global url_q2_1
url_q2='http://vip.stock.finance.sina.com.cn/corp/go.php/vCB_BulletinZhong/stockid/002271/page_type/zqbg.phtml'
url_q2_1='http://vip.stock.finance.sina.com.cn/corp/go.php/vCB_Bulletin/stockid/'
url_q2_2='/page_type/zqbg.phtml'

global url_q3_1
url_q3='http://vip.stock.finance.sina.com.cn/corp/go.php/vCB_BulletinSan/stockid/002271/page_type/sjdbg.phtml'
url_q3_1='http://vip.stock.finance.sina.com.cn/corp/go.php/vCB_Bulletin/stockid/'
url_q3_2='/page_type/sjdbg.phtml'

# global url_zhaogu
# url_zhaogu_sample='http://vip.stock.finance.sina.com.cn/corp/view/vCB_Bulletin.php/page_type/zgsmsyxs.phtml?stockid=002271'
url_zhaogu_sample='http://vip.stock.finance.sina.com.cn/corp/go.php/vCB_BulletinSan/stockid/002271/page_type/zgsmsyxs.phtml'
# url_zhaogu='http://vip.stock.finance.sina.com.cn/corp/view/vCB_Bulletin.php/page_type/zgsmsyxs.phtml?stockid='
url_zhaogu_1='http://vip.stock.finance.sina.com.cn/corp/go.php/vCB_Bulletin/stockid/'
url_zhaogu_2='/page_type/zgsmsyxs.phtml'

#下载文件目录
global downloadpath1 #,downloadpath2


#downloadpath1='C://Users//aaron//Documents//' #(PLRWorkStatiun)
#
#下载文件命名规格
global filename_ar,filename_q1,filename_q2,filename_q3,filename_zhaogu
filename_ar_sample='002271_2018_年度报告'
filename_ar='_年度报告'

filename_q1_sample='002271_2018_一季报告'
filename_q1='_一季报告'

filename_q2_sample='002271_2018_年中报告'
filename_q2='_年中报告'

filename_q3_sample='002271_2018_三季报告'
filename_q3='_三季报告'

filename_zhaogu_sample='002271_招股说明书'
filename_zhaogu='_招股说明书'


#错误提示
global msg1, msg2,msg3
msg1='没有此时的报表，无法下载'
msg2='文件已存在，是否要覆盖？'
msg3="未找到该代码"

#当前文件的路径
pwd = os.getcwd()
print(pwd)
#当前文件的父路径
father_path=os.path.abspath(os.path.dirname(pwd)+os.path.sep+".")
print(father_path)
# 更换stocklist目录，放到代码同一个目录中
# stocklistwholepath=father_path + "/MyTSSnippets/DataRepository/db00021/stocklist2.csv"
stocklistwholepath=pwd + '/ts00061 财报下载/stocklist.csv'
print(stocklistwholepath)
fullstocklistwholepath=pwd + "/DataRepository/db00011/stockcodelist1.csv"
print(fullstocklistwholepath)