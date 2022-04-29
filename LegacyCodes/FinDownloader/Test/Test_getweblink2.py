

# -*- coding: utf-8 -*-

#读取html文件
# 从新浪财经获取PDF
import re
import requests
from bs4 import BeautifulSoup
import lxml
import urllib
import os
import  csv

from GlobalParameters import filename_ar,filename_q2,filename_q1,filename_q3,filename_zhaogu,\
                                downloadpath1,url_ar_1, url_ar_2, \
                                url_q1_1,url_q1_2,url_q2_1,url_q2_2,\
                                url_q3_1, url_q3_2, \
                                url_zhaogu_1,url_zhaogu_2\


codenumber='002271'
downloadtype=4  #4-年报；1-1季报；2-中报；3-3季报；5-招股; 0-4个季度报表全部下载
downloadflag=True  #True为实际下载，False为不下载
debugflag=False      #True为输出调试信息，False为不输出

headers1={"User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10.13; rv:55.0) Gecko/20100101 Firefox/55.0"}
send_headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36",    "Connection": "keep-alive",    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",    "Accept-Language": "zh-CN,zh;q=0.8"    }



def DownloadFR(downloadtype):
    return 1

if downloadtype==4:
    realurl=url_ar_1 +codenumber + url_ar_2
    filetypestr = filename_ar
elif downloadtype==1:
    realurl=url_q1_1 + codenumber + url_q1_2
    filetypestr = filename_q1
elif downloadtype==2:
    realurl=url_q2_1 + codenumber+ url_q2_2
    filetypestr = filename_q2
elif downloadtype==3:
    realurl=url_q3_1 + codenumber+ url_q3_2
    filetypestr = filename_q3
elif downloadtype==5:
    realurl=url_zhaogu_1 + codenumber+url_zhaogu_2
    filetypestr = filename_zhaogu

if debugflag==True:
    print(url_q1_1 + codenumber)


r = requests.get(realurl,timeout=10,headers=send_headers)
r.encoding = 'gbk'
r.close()

soup=BeautifulSoup(r.text,'lxml')

# regex_str=
# print(soup.prettify())

#关键代码
datelist=soup.find('div',class_="datelist").find_all('a') #不是用find_all("href")

# ########################读取代码和名称的字典文件
with open('../StockList.csv',newline='') as csv_file:
    csv_reader = csv.DictReader(csv_file,fieldnames=['code','name'])
    dict={}
    for row in csv_reader:
        dict[row['code']]=row['name']
    if debugflag==True:
        print(dict[codenumber])

for eachaddress in datelist:
    if debugflag==True:
        print(eachaddress.text)
    # yearnumber=re.search(r"(2[]+年)",eachaddress.text)
    if downloadtype==1 or downloadtype==2 or downloadtype==3 or downloadtype==4:
        yearnumber = re.search(r'(\d{4})',eachaddress.text)
        if debugflag == True:
            print("yearnumber" + yearnumber.group(1))
    elif downloadtype==5:
        yearnumber='招股说明书'


    # print(eachaddress.text + ':' + 'http://vip.stock.finance.sina.com.cn/' + eachaddress.get('href'))
    PDFWebpage='http://vip.stock.finance.sina.com.cn/' + eachaddress.get('href')


    if debugflag == True:
        print(filetypestr)

    #招股说明书无法在新浪这个网站下载PDF，也许只能下载HTML格式文件
    if downloadtype==1 or downloadtype==2 or downloadtype==3 or downloadtype==4:
        r = requests.get(PDFWebpage, timeout=10, headers=send_headers)
        r.encoding = 'gbk'
        r.close()

        soup = BeautifulSoup(r.text, 'lxml')

        PDFAddress=soup.find('table',id="allbulletin").find('a').get('href')
        if debugflag == True:
            print(PDFAddress)
        filename=os.path.basename(PDFAddress)
        downloadpath2=downloadpath1 + codenumber + ' ' + dict[codenumber] + '//'

        if debugflag == True:
            print(downloadpath2)
        # filepathname='../../../' + codenumber + '_' +dict[codenumber] +'_' + yearnumber.group(0) + filetypestr + '.pdf' #+ filename
        filepathname=downloadpath2 + codenumber + '_' +dict[codenumber] +'_' + yearnumber.group(0) + filetypestr + '.pdf'  #+ filename

        if debugflag==True:
            print(filepathname)

        if downloadflag==True:
            urllib.request.urlretrieve(PDFAddress, filename=filepathname)



#得到如下内容，从中提取href文本
# http://vip.stock.finance.sina.com.cn/corp/view +以下内容
#[<div class="datelist">
#      <ul>
# 			2019-03-28 <a href="/corp/view/vCB_AllBulletinDetail.php?stockid=002271&amp;id=5118961" target="_blank">东方雨虹：2018年年度报告</a><br/>
# 			2018-04-24 <a href="/corp/view/vCB_AllBulletinDetail.php?stockid=002271&amp;id=4309197" target="_blank">东方雨虹：2017年年度报告</a><br/>
# 			2017-04-21 <a href="/corp/view/vCB_AllBulletinDetail.php?stockid=002271&amp;id=3265799" target="_blank">东方雨虹：2016年年度报告</a><br/>
# 			2016-04-23 <a href="/corp/view/vCB_AllBulletinDetail.php?stockid=002271&amp;id=2394374" target="_blank">东方雨虹：2015年年度报告</a><br/>
# 			2015-04-28 <a href="/corp/view/vCB_AllBulletinDetail.php?stockid=002271&amp;id=1754542" target="_blank">北京东方雨虹防水技术股份有限公司2014年年度报告</a><br/>
# 			2014-03-18 <a href="/corp/view/vCB_AllBulletinDetail.php?stockid=002271&amp;id=1319510" target="_blank">北京东方雨虹防水技术股份有限公司2013年年度报告</a><br/>
# 			2013-04-13 <a href="/corp/view/vCB_AllBulletinDetail.php?stockid=002271&amp;id=1090780" target="_blank">北京东方雨虹防水技术股份有限公司2012年年度报告</a><br/>
# 			2012-04-13 <a href="/corp/view/vCB_AllBulletinDetail.php?stockid=002271&amp;id=881574" target="_blank">北京东方雨虹防水技术股份有限公司2011年年度报告</a><br/>
# 			2011-04-23 <a href="/corp/view/vCB_AllBulletinDetail.php?stockid=002271&amp;id=708836" target="_blank">北京东方雨虹防水技术股份有限公司2010年年度报告</a><br/>
# 			2010-01-30 <a href="/corp/view/vCB_AllBulletinDetail.php?stockid=002271&amp;id=504805" target="_blank">北京东方雨虹防水技术股份有限公司2009年年度报告</a><br/>
# 	    </ul>
# </div>]

# for eachdate in datelist.find('a'):
#     print(eachdate)

# for each in soup.find('div',class_="datelist")
#PageUrl="https://www.lixinger.com/analytics/company/sz/300383/detail/announcement?announcement-type=fs&page-index=0"

#file_url = re.search('http://file.finance.sina.com.cn/211.154.219.97:9494/.*?PDF',PageUrl)


if downloadtype==0:
    DownloadFR(1)
    DownloadFR(2)
    DownloadFR(3)
    DownloadFR(4)