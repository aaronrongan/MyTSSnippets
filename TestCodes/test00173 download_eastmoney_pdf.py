#从东方财富下载招股�?明书
#仿照新浪财经的方�?
#如何在一�??个tab形式的网页中找到需要的pdf文件

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
#错�?提示

#下载地址

# global url_zhaogu
# url_zhaogu_sample='http://vip.stock.finance.sina.com.cn/corp/view/vCB_Bulletin.php/page_type/zgsmsyxs.phtml?stockid=002271'
# url_zhaogu_sample='http://vip.stock.finance.sina.com.cn/corp/go.php/vCB_BulletinSan/stockid/002271/page_type/zgsmsyxs.phtml'
# url_zhaogu='http://vip.stock.finance.sina.com.cn/corp/view/vCB_Bulletin.php/page_type/zgsmsyxs.phtml?stockid='
# url_zhaogu_1='http://vip.stock.finance.sina.com.cn/corp/go.php/vCB_Bulletin/stockid/'
# url_zhaogu_2='/page_type/zgsmsyxs.phtml'

url_zhaogu_1='http://data.eastmoney.com/notices/stock/002271.html'


#下载文件�?��
global downloadpath1 #,downloadpath2


#downloadpath1='C://Users//aaron//Documents//' #(PLRWorkStatiun)
#
#下载文件命名规格

filename_zhaogu_sample='002271_招股说明�?'
filename_zhaogu='_招股说明�?'


#错�?提示
global msg1, msg2,msg3
msg1='没有此时的报�?��无法下载'
msg2='文件已存�?���?��要�?盖？'
msg3="�?��到�?代码"

#当前文件的路�?
pwd = os.getcwd()
#当前文件的父�?��
father_path=os.path.abspath(os.path.dirname(pwd)+os.path.sep+".")

# 更换stocklist�?��，放到代码同一�?��录中
# stocklistwholepath=father_path + "/MyTSSnippets/DataRepository/db00021/stocklist2.csv"
stocklistwholepath=pwd + '/ts00061 财报下载/stocklist.csv'
fullstocklistwholepath=father_path + "/MyTSSnippets/DataRepository/db00011/stockcodelist1.csv"


def PrepardDownloadPath(strPath):
    if not os.path.exists(strPath):
        os.mkdir(strPath)

#参数说明
#   codenumber = '002271'

def DownloadFR(codenumber,downloadflag,debugflag):

    headers1 = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.13; rv:55.0) Gecko/20100101 Firefox/55.0"}
    send_headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36",
        "Connection": "keep-alive",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
        "Accept-Language": "zh-CN,zh;q=0.8"}


    realurl = url_zhaogu_1 #+ codenumber 
    filetypestr = filename_zhaogu

    if debugflag == True:
        print(realurl)

    r = requests.get(realurl, timeout=10, headers=send_headers)
    r.encoding = 'gbk'
    print(r.text)
    r.close()
    if debugflag==True:
        print(r)

    soup = BeautifulSoup(r.text, 'lxml')

    # regex_str=
    # print(soup.prettify())

    # 关键代码
    try:
        pdflist = soup.find('div', class_="datelist").find_all('a')  # 不是用find_all("href")
    except:
        print("�?��到地址"+ "；代码：" + codenumber)
        return

   # global yearnumber
    # ########################读取代码和名称的字典文件,包括所有代码在�?,用Full.csv
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

    # #分析每年，eachaddress为单年年�?
    # for eachaddress in datelist:
    #     try:
    #         yearnumber='0'
    #         if debugflag == True:
    #             print(eachaddress.text)
    #         # yearnumber=re.search(r"(2[]+�?)",eachaddress.text)
    #         if downloadtype == '1' or downloadtype == '2' or downloadtype == '3' or downloadtype == '4':
    #             yearnumber = re.search(r'(\d{4})', eachaddress.text)
    #             if debugflag == True:
    #                 #print("yearnumber" + yearnumber.group(1))
    #                 print("yearnumber" + yearnumber.group(0))
    #         elif downloadtype == '5':
    #             yearnumber = '招股说明�?'
    #     except AttributeError as e:
    #         print("except: �?��到链接地址。代�?:" + dict1[codenumber])
    #         break

       
        #try:
    
    # if debugflag == True:
    #     print(eachaddress.text + ':' + 'http://vip.stock.finance.sina.com.cn/' + eachaddress.get('href'))

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

                #判断文件夹是否存�?��如果不存�?��则创建�?�?��
            PrepardDownloadPath(downloadpath1 + codenumber + ' ' + dict1[codenumber])

            if debugflag == True:
                print(downloadpath2)
            # filepathname='../../../' + codenumber + '_' +dict[codenumber] +'_' + yearnumber.group(0) + filetypestr + '.pdf' #+ filename
            filepathname = downloadpath2 + codenumber + '_' + dict1[codenumber] + '_' + yearnumber.group(
                0) + filetypestr + '.pdf'  # + filename

            if debugflag == True:
                print(filepathname)


            # 判断该文件是否存�?
            if os.path.exists(filepathname):
                print(codenumber + "文件已存�?!")
            else:
                if downloadflag == True:
                    #此�?条件夹文�?
                    #print("准�?下载" + PDFAddress)
                    try:
                        urllib.request.urlretrieve(PDFAddress, filename=filepathname)
                        print("已下�?" + PDFAddress)
                    except:
                        print("下载地址有�?，无法下�?")
        except AttributeError as e:
            print("except: �?��到PDF链接地址" )
    #except:#
        #print("attribute 错�?")

def getlocaldownloadpath():
    hostname=socket.gethostname()
    if hostname=='MyWorkstation':
        return 'I://MyMobileBooks_800_FinRep//' #MyWorkStation
    elif hostname=='MyMacWin10':
        return 'C:/Users/aaron/Documents/MyMobileBooks_800_FinRep/'
    elif hostname=="DESKTOP-DEFM935":
        return 'C:/FinReport/'
    else:
        print('not in defined disk')
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
    #     print('not in defined disk')
    #     exit()

    codenumber=str(input('输入代码�?0-根据StockList.csv; 其它-根据实际代码:;[0]'))
    if codenumber=='':
        codenumber='0'
    # yeartype1=str(input('输入年份: 0-所有年；其�?-实际年份;[0]:'))
    # if yeartype1=='':
    #     yeartype1='0'
    # downloadtype1=str(input('输入年报类型�?0-所有财�?; 1-一季报�?2-�?���?3-三�?�?;4-年报；[0]:'))
    # if downloadtype1=='':
    #     downloadtype1='0'
    downloadflag1=str(input('�?��下载还是仅仅测试而不下载:0-不下�?;1-下载;[1]'))
    if downloadflag1=='1' or downloadflag1=='':
        downloadflag1=True
    else:
        downloadflag1 = False
    verboseflag=str(input('�?��输出�?��信息�?1-输出调试信息�?0-不输出调试信�?;[1]:'))
    if verboseflag=='1' or verboseflag=='':
        verboseflag=True
    else:
        verboseflag = False

    #os.path.dirname(os.path.abspath('.'))

  
    # with open('./StockList.csv', newline='', encoding = 'UTF-8-sig') as csv_file:
    with open(stocklistwholepath, newline='', encoding = 'UTF-8-sig') as csv_file:
        # with open('StockList.csv',newline='', encoding = 'UTF-8',errors='ignore') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        for row in csv_reader:
            # print(row['code'],row['name'])
            # codelist.append(row['code'])
            print(row)
            print(row['code'])
            
            DownloadFR(codenumber=row['code'], downloadflag=downloadflag1,
                            debugflag=verboseflag)
                
    # csv_file.close()
   