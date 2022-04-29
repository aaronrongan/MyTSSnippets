# # 从cninfo下载招股说明书下载地址。其实年报也是可以下载的，但是要考虑翻页的问题。参考别人的代码
# # 要点
# - 正则表达式，找出不含有某个字符串。目前用一个比较锉的方法来实现。
# - 在Jason中找到需要的字段json.loads(r.text).get('announcements').get....
# - Logging的运用
# - 网络文件的下载
# # 参考文件
# 用LogFile来记录
# test00175 download_cninfo

# nextstep


import csv
import math
import os
import time
import requests
import json
import urllib
import socket
import sys
import logging

# logging.basicConfig(filename="test.log", filemode="w", format="%(asctime)s %(name)s:%(levelname)s:%(message)s", datefmt="%d-%M-%Y %H:%M:%S", level=logging.DEBUG) #这里"%d-%M-%Y 有错误，无法正确显示日期
logging.basicConfig(filename="test.log", filemode="w", format="%(asctime)s %(name)s:%(levelname)s:%(message)s", datefmt='%Y-%b-%d %H:%M:%S', level=logging.DEBUG) # %a, 显示周几
logging.debug('This is a debug message')
logging.info('This is an info message')
logging.warning('This is a warning message')
logging.error('This is an error message')
logging.critical('This is a critical message')

#当前文件的路径
pwd = os.getcwd()
#当前文件的父路径
father_path=os.path.abspath(os.path.dirname(pwd)+os.path.sep+".")


# 更换stocklist目录，放到代码同一个目录中
# stocklistwholepath=father_path + "/MyTSSnippets/DataRepository/db00021/stocklist2.csv"
stocklistwholepath=pwd + '/ts00341 招股说明书下载/stocklist.csv'
# fullstocklistwholepath=father_path + "/MyTSSnippets/DataRepository/db00011/stockcodelist1.csv"
fullstocklistwholepath="C:\\Users\\Aaron\\Documents\\MyMobileBooks_800_Reading\\MyTSSnippets\\DataRepository\\db00011\\stockcodelist1.csv"

headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.13; rv:55.0) Gecko/20100101 Firefox/55.0"}
   
#sample:
# realurl='http://www.cninfo.com.cn/new/fulltextSearch/full?searchkey=300383+招股&sdate=&edate=&isfulltext=false&sortName=pubdate&sortType=desc&pageNum=1'
realurl_front='http://www.cninfo.com.cn/new/fulltextSearch/full?searchkey='
realurl_rear='+招股&sdate=&edate=&isfulltext=false&sortName=pubdate&sortType=desc&pageNum=1'

# 股票代码、名称字典，在程序运行时自动生成3000个左右的字典
codelistdict={}

def GetPDFUrl(codenumber):
    try:
        url=""
        queryurl=realurl_front + codenumber + realurl_rear
        r = requests.get(queryurl, timeout=10, headers=headers)

        # print(r.text)

        #realurl2='http://www.cninfo.com.cn/new/announcement/bulletin_detail?announceId=21090184&flag=false&announceTime=2007-02-28%2006:30'
        #r2 = requests.get(realurl, timeout=10, headers=headers)
        #print(r2.text)

        #state=json.loads(r.text).get('classifiedAnnouncements').get('announcements')
        annlists=json.loads(r.text).get('announcements')
        for each in annlists:
            print(each.get('announcementTitle')) #列出所有的搜索列表
            #下面的语句比较锉，以后尝试用正则表达式实现
            # if each.get('announcementTitle').find('首次公开发行')>=0 :
            # or each.get('announcementTitle').find('招股书')>=0 
            if each.get('announcementTitle').find('招股</em>说明书')>=0:
                if each.get('announcementTitle').find('摘要')<0 :
                    if each.get('announcementTitle').find('附录')<0 :
                        # print(each.get('announcementTitle'))
                        url=each.get('adjunctUrl')
                        break

        if url!="":
            fullurl='http://static.cninfo.com.cn/' + url
            return fullurl
        else:
            logging.log(level=logging.DEBUG,msg="未找到招股说明书文件:"+codenumber + ' '+ codelistdict[codenumber])
            return ""
    except:
        # print('未找到招股说明书文件')
        logging.log(level=logging.DEBUG,msg="未找到招股说明书文件:"+codenumber + ' '+ codelistdict[codenumber])
        return ""       

def GetLocalDownloadPath():
    hostname=socket.gethostname()
    if hostname=='MyWorkstation':
        # return 'I://MyMobileBooks_800_FinRep//' #MyWorkStation
        return 'E://=ICH//==Library//MyMobileBooks_800_FinRep//' #MyWorkStation
    elif hostname=='MyMacWin10':
        return 'C:/Users/aaron/Documents/MyMobileBooks_800_FinRep/'
    elif hostname=="DESKTOP-DEFM935":
        return 'C:/FinReport/'
    elif hostname=="MY2570P":
        return 'C:/MyMobileBooks_800_FinRep/'
    elif hostname=="MY8560W":
        return 'C:/MyMobileBooks_800_FinRep/'
    else:
        # print('not in defined disk')
        logging.log(level=logging.DEBUG,msg="未找到本地下载路径" +codenumber + ' '+ codelistdict[codenumber])
        return '0'

#生成代码和名称字典codelistdict
def MakeCodeNumberDict():
     with open(fullstocklistwholepath, newline='',encoding = 'UTF-8-sig') as csv_file:
        csv_reader = csv.DictReader(csv_file, fieldnames=['code', 'name'])
        for row in csv_reader:
            # print(row['name'])
            codelistdict[row['code']] = row['name']

def PrepardDownloadPath(strPath):
    if not os.path.exists(strPath):
        os.mkdir(strPath)

def SavetoLocalfile(downloadurl, codenumber):

    if downloadurl=="":
        logging.log(logging.DEBUG,msg="文件地址为空:" + codenumber + ' '+ codelistdict[codenumber])
    else:
        try:
            codename=codelistdict[codenumber]
        except:
            logging.log(logging.DEBUG,msg="找不到该代码："+codenumber + ' '+ codelistdict[codenumber])
            return

        downloadpath1=GetLocalDownloadPath()+ codenumber +' ' +  codename + '//'

        #判断文件夹是否存在，如果不存在，则创建该目录
        PrepardDownloadPath(downloadpath1)

        filename= downloadpath1 + codenumber +'_' +  codename + '_招股说明书.pdf'

        print(filename)

        if not os.path.exists(filename):
            try:
                urllib.request.urlretrieve(downloadurl,filename)
            except:
                logging.log(level=logging.DEBUG,msg="无法下载文件:"+codenumber + ' '+ codelistdict[codenumber])
        else:
            logging.log(level=logging.DEBUG,msg="文件已存在:"+codenumber + ' '+ codelistdict[codenumber])

if __name__=="__main__":
    MakeCodeNumberDict()

    downloadpath1=GetLocalDownloadPath()
    if downloadpath1=='0':
        sys.exit()

    codenumber=str(input('输入代码：0-根据StockList.csv; 其它-根据实际代码:;[0]'))
    if codenumber=='':
        codenumber='0'
    print(codenumber)
    # queryurl=realurl_front + '300383' + realurl_rear 
    # codenumber = '0'

    if codenumber != '0':
        downloadurl=GetPDFUrl(codenumber)
        # print(downloadurl)
        
        SavetoLocalfile(downloadurl,codenumber)
        
    elif codenumber=='0':
        # print(stocklistwholepath)
        with open(stocklistwholepath, newline='', encoding = 'UTF-8-sig') as csv_file:
            csv_reader = csv.DictReader(csv_file)
            print(csv_reader)
            for row in csv_reader:
                print(row['code'])
                
                downloadurl=GetPDFUrl(row['code'])
                print(downloadurl)
                
                SavetoLocalfile(downloadurl,row['code'])
               



