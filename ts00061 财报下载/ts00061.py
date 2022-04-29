
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
# fullstocklistwholepath=pwd + "/DataRepository/db00011/stockcodelist1.csv"
fullstocklistwholepath="C:\\Users\\Aaron\\Documents\\MyMobileBooks_800_Reading\\MyTSSnippets\\DataRepository\\db00011\\stockcodelist1.csv"

print(fullstocklistwholepath)
# /MyTSSnippets

# from setting import filename_ar, filename_q2, filename_q1, filename_q3, filename_zhaogu, \
#     downloadpath1, url_ar_1, url_ar_2, \
#     url_q1_1, url_q1_2, url_q2_1, url_q2_2, \
#     url_q3_1, url_q3_2, \
#     url_zhaogu_1, url_zhaogu_2

# from setting import msg1, msg2, msg3


def PrepardDownloadPath(strPath):
    if not os.path.exists(strPath):
        os.mkdir(strPath)

#参数说明
#   codenumber = '002271'
#   downloadtype = ’4‘  # 4-年报；1-1季报；2-中报；3-3季报；5-招股; 0-4个季度报表全部下载
#   downloadflag = True  # True为实际下载，False为不下载
#   debugflag = False  # True为输出调试信息，False为不输出
#   yeartype 年度, 为’0‘则下载所有报表 #

def DownloadFR(downloadtype,yeartype,codenumber,downloadflag,debugflag):

    headers1 = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.13; rv:55.0) Gecko/20100101 Firefox/55.0"}
    send_headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36",
        "Connection": "keep-alive",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
        "Accept-Language": "zh-CN,zh;q=0.8"}

    if downloadtype == '4':
        realurl = url_ar_1 + codenumber + url_ar_2
        filetypestr = filename_ar
    elif downloadtype == '1':
        realurl = url_q1_1 + codenumber + url_q1_2
        filetypestr = filename_q1
    elif downloadtype == '2':
        realurl = url_q2_1 + codenumber + url_q2_2
        filetypestr = filename_q2
    elif downloadtype == '3':
        realurl = url_q3_1 + codenumber + url_q3_2
        filetypestr = filename_q3
    elif downloadtype == '5':
        realurl = url_zhaogu_1 + codenumber + url_zhaogu_2
        filetypestr = filename_zhaogu
    else:
        realurl = url_ar_1 + codenumber + url_ar_2
        filetypestr = filename_ar

    if debugflag == True:
        print(realurl)

    r = requests.get(realurl, timeout=10, headers=send_headers)
    r.encoding = 'gbk'
    r.close()
    if debugflag==True:
        print(r)

    soup = BeautifulSoup(r.text, 'lxml')

    # regex_str=
    # print(soup.prettify())

    # 关键代码
    #找到显示的各年度
    try:
        datelist = soup.find('div', class_="datelist").find_all('a')  # 不是用find_all("href")
    except:
        print("未找到地址。年度："+ yeartype + "；代码：" + codenumber)
        return

   # global yearnumber
    # ########################读取代码和名称的字典文件,包括所有代码在内,用Full.csv
    with open(fullstocklistwholepath, newline='',encoding = 'UTF-8-sig') as csv_file:
        csv_reader = csv.DictReader(csv_file, fieldnames=['code', 'name'])

        # print(csv_reader)

        dict1 = {}
        for row in csv_reader:
            # print(row['name'])
            dict1[row['code']] = row['name']

        # print(len(dict1()))

        if dict1[codenumber]!="":
            if debugflag == True:
                print(dict1[codenumber])
            else:
                print(msg3)
    csv_file.close()

    #分析每年，eachaddress为单年年份
    for eachaddress in datelist:
        try:
            yearnumber='0'
            if debugflag == True:
                print(eachaddress.text)
            # yearnumber=re.search(r"(2[]+年)",eachaddress.text)
            if downloadtype == '1' or downloadtype == '2' or downloadtype == '3' or downloadtype == '4':
                yearnumber = re.search(r'(\d{4})', eachaddress.text)
                if debugflag == True:
                    #print("yearnumber" + yearnumber.group(1))
                    print("yearnumber" + yearnumber.group(0))
            elif downloadtype == '5':
                yearnumber = '招股说明书'
        except AttributeError as e:
            print("except: 未找到链接地址。代码:" + dict1[codenumber])
            break

        #当输入年份为0时，需要所有的年份，
        #当输入年份不为0而且和找到的年份不相同时，则跳过
        #try:
        if yeartype!= yearnumber.group(0) and yeartype !='0':
        # BUG：yeartype1为0时，无法下载
        # 原因：yeartype!="0" 应该是!=0，包括downloadtype的字符串也是容易混淆成数字
            if debugflag==True:
                print("jump out")
            continue
        #需要单独某年
        else:
            if debugflag == True:
                print(eachaddress.text + ':' + 'http://vip.stock.finance.sina.com.cn/' + eachaddress.get('href'))

            PDFWebpage = 'http://vip.stock.finance.sina.com.cn/' + eachaddress.get('href')

            if debugflag == True:
                print(filetypestr)

            # 招股说明书无法在新浪这个网站下载PDF，也许只能下载HTML格式文件
            if downloadtype == '1' or downloadtype == '2' or downloadtype == '3' or downloadtype == '4':
                r = requests.get(PDFWebpage, timeout=10, headers=send_headers)
                r.encoding = 'gbk'
                r.close()

                soup = BeautifulSoup(r.text, 'lxml')
                #print(soup.text)
                try:
                    PDFAddress = soup.find('table', id="allbulletin").find('a').get('href')
                    if debugflag == True:
                        print(PDFAddress)
                    # filename = os.path.basename(PDFAddress)
                    downloadpath2 = downloadpath1 + codenumber + ' ' + dict1[codenumber] + '//'

                     #判断文件夹是否存在，如果不存在，则创建该目录
                    PrepardDownloadPath(downloadpath1 + codenumber + ' ' + dict1[codenumber])

                    if debugflag == True:
                        print(downloadpath2)
                    # filepathname='../../../' + codenumber + '_' +dict[codenumber] +'_' + yearnumber.group(0) + filetypestr + '.pdf' #+ filename
                    filepathname = downloadpath2 + codenumber + '_' + dict1[codenumber] + '_' + yearnumber.group(
                        0) + filetypestr + '.pdf'  # + filename

                    if debugflag == True:
                        print(filepathname)

                   

                    # 判断该文件是否存在
                    if os.path.exists(filepathname):
                        print(codenumber + '的' + yearnumber.group(0) + "年第" + downloadtype +"季度文件已存在!")
                    else:
                        if downloadflag == True:
                            #此处条件夹文件
                            #print("准备下载" + PDFAddress)
                            try:
                                urllib.request.urlretrieve(PDFAddress, filename=filepathname)
                                print("已下载" + PDFAddress)
                            except:
                                print("下载地址有误，无法下载")
                except AttributeError as e:
                    print("except: 未找到PDF链接地址" )
        #except:#
            #print("attribute 错误")

def getlocaldownloadpath():
    hostname=socket.gethostname()
    if hostname=='MyWorkstation':
        #return 'I://MyMobileBooks_800_FinRep//' #MyWorkStation
        return 'E://=ICH//==Library//MyMobileBooks_800_FinRep//' #MyWorkStation
    elif hostname=='MyMacWin10':
        return 'C:/Users/aaron/Documents/MyMobileBooks_800_FinRep/'
    elif hostname=="DESKTOP-DEFM935":
        return 'D:/MyMobileBooks_800_FinRep/'
    elif hostname=="PLRWORKSTATION":
        return 'C:/Users/Administrator/Documents/MyMobileBooks_800_FinRep/'
    elif hostname=="MyPortBook":
        return 'C:/Users/aaron/Documents/MyMobileBooks_800_FinRep/'
    else:
        print('Error:not in defined disk')
        return '0'

if __name__=="__main__":
    codelist=[]

    downloadpath1=getlocaldownloadpath()
    if downloadpath1=='0':
        sys.exit()

    # hostname=socket.gethostname()
    # if hostname=='MyWorkstation':
    #     downloadpath1='I://MyMobileBooks_800_FinRep//' #MyWorkStation
    # elif hostname=='MyMacWin10':
    #     downloadpath1='C:/Users/aaron/Documents/MyMobileBooks_800_FinRep/'
    # else:
    #     print(' not in defined disk')
    #     exit()

    codenumber=str(input('输入代码：0-根据StockList.csv; 其它-根据实际代码:;[0]'))
    if codenumber=='':
        codenumber='0'
    yeartype1=str(input('输入年份: 0-所有年；其它-实际年份;[0]:'))
    if yeartype1=='':
        yeartype1='0'
    downloadtype1=str(input('输入年报类型：0-所有财报; 1-一季报；2-中报；3-三季报;4-年报；[0]:'))
    if downloadtype1=='':
        downloadtype1='0'
    downloadflag1=str(input('是否下载还是仅仅测试而不下载:0-不下载;1-下载;[1]'))
    if downloadflag1=='1' or downloadflag1=='':
        downloadflag1=True
    else:
        downloadflag1 = False
    verboseflag=str(input('是否输出中间信息：1-输出调试信息；0-不输出调试信息;[1]:'))
    if verboseflag=='1' or verboseflag=='':
        verboseflag=True
    else:
        verboseflag = False

    #os.path.dirname(os.path.abspath('.'))

    if codenumber =='0' :
        # with open('./StockList.csv', newline='', encoding = 'UTF-8-sig') as csv_file:
        with open(stocklistwholepath, newline='', encoding = 'UTF-8-sig') as csv_file:
            # with open('StockList.csv',newline='', encoding = 'UTF-8',errors='ignore') as csv_file:
            csv_reader = csv.DictReader(csv_file)
            for row in csv_reader:
                # print(row['code'],row['name'])
                # codelist.append(row['code'])
                print(row)
                print(row['code'])
                if downloadtype1 == '0':
                    for each in range(1, 5):
                        DownloadFR(str(each), yeartype=yeartype1, codenumber=row['code'], downloadflag=downloadflag1,
                                debugflag=verboseflag)
                else:
                    DownloadFR(downloadtype1, yeartype=yeartype1, codenumber=row['code'], downloadflag=downloadflag1,
                            debugflag=verboseflag)
        csv_file.close()
    else:
        #下载4个季度财报,循环
        if downloadtype1=='0':
            for each in range(1, 5):
                DownloadFR(str(each), yeartype=yeartype1, codenumber=codenumber, downloadflag=downloadflag1, debugflag=verboseflag)
        #下载单季财报
        else:
            DownloadFR(downloadtype1, yeartype=yeartype1, codenumber=codenumber, downloadflag=downloadflag1, debugflag=verboseflag)