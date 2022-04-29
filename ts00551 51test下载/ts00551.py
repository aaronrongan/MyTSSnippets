#!/usr/bin/env python
# coding: utf-8

# -*- coding: utf-8 -*-
# 
# ## 目的：
# 下载51test等网站的word考试卷、辅导材料等
# 
# ## 参考资料：
# https://www.51test.net/
# cninfo巨潮网下载年报
# 0daydownscrap
# 
# ## 重点：
# 翻页
# BeautifulSoup
# requests
# 
# * Firefox driver的设置
# 
# profile = webdriver.firefox.firefox_profile.FirefoxProfile(profileDir)
# 
# 
# profile.set_preference('browser.download.folderList',2)
# profile.set_preference('browser.download.manager.showWhenStarting', True)
# profile.set_preference('browser.download.dir','C:\\Users\\Administrator\\Downloads\\51test')
# profile.set_preference('browser.helperApps.neverAsk.saveToDisk','application/vnd.openxmlformats-officedocument.wordprocessingml.document,application/msword,application/vnd.ms-word,application/zip,text/plain,application/vnd.ms-excel,text/csv,text/comma-separated-values,application/octet-stream,application/vnd.openxmlformats-officedocument.spreadsheetml.sheet,application/vnd.openxmlformats-officedocument.wordprocessingml.document,application/xml,text/plain,text/xml,text/doc,text/docx,image/jpeg,text/csv,application/octet-stream,text/html,application/x-msdownload,application/zip,application/kswps,application/pdf,application/doc,application/docx')
# 
# profile.set_preference("browser.altClickSave", True)
# profile.update_preferences()
# 
# driver = webdriver.Firefox(firefox_profile=profile)
# 
# * chrome driver的设置
# driverOptions = webdriver.ChromeOptions()
# driverOptions.add_argument(r"user-data-dir=C:\Users\Administrator\Downloads\51test\GoogleProfile")
# chrome_driver='C:/Users/Administrator/Downloads/chromedriver.exe'

# 
# driver = webdriver.Chrome(executable_path=chrome_driver,options=driverOptions)
# 
# * 找到弹出的页面
# 其实是一个frame
# iframes =driver.find_elements_by_xpath("//iframe")
# print(len(iframes))
# driver.switch_to.frame(0)
# 
# * 将selenium找到的页面交给Beautiful Soup分析
# soup = BeautifulSoup(driver.page_source, "lxml")
# 
# * 网页文件有2种形式，一种是已经生成的，一种是需要现场convert的；
# 前者需要用beautifulsoup获取地址即可
# 后者需要用selenium获取按钮，然后
# 
# ## 算法：
# 1. 配置Chrome driver
# 
# 2. 给定一个网页链接，比如“高考满分作文”，下载该专题
# https://www.51test.net/gaokao/manfenzuowen/
# 
# 3. 遍历获取每个文件的链接页面，如https://www.51test.net/show/9870584.html，获得ID号码
# 
# 4. 获取下载页面
# https://user.51test.net/vip/download/word/?id=9870584
# 
# 预览的页面为：
# url='https://view.51test.net/docview/?id=9870584' #这个页面是弹出word预览的页面，该页面里包含https://view.51test.net/word/?id=9870584&token=5bfc85dd27e114081435b41830a0fc2e信息
# 
# 5. 实际的页面有2种，一个是静态地址，一个是动态地址
# 
# 
# ## 流程
# 分析版面页面，抓取实际链接
# |
# 获取所有页面从1~13页的链接，进行searchkey的中文处理
# |
# 对每个页面进行分析，获取dict，文件编码和文件名称
# |
# 进入下载页面，弹出页面
# |
# 下载文件，保存
# |
# 进行下一个页面的分析
# 
# ## 进阶：
# 一次性爬取所有试卷信息
# ============================
# 通过修改Firefox设置配置下载不做选择，直接下载到某个目录
# 
# http://www.mamicode.com/info-detail-1283143.html
# https://blog.csdn.net/qq_22821275/article/details/72880323
# 
# 第二步：修改Firefox的相关配置。
# 
# profile.set_preference('browser.download.folderList',2)    
# 
# #设置成0代表下载到浏览器默认下载路径；设置成2则可以保存到指定目录
# 
# profile.set_preference('browser.download.dir','F:\\Users')  
# 
# #保存到指定目录F盘Users文件夹。可以任意文件夹，但是记得分隔符是两个反斜杠
# 
# profile.set_preference('browser.download.manager.showWhenStarting',False)
# 
# #不管是True还是False，都不显示开始，直接开始下载
# 
# profile.set_preference('browser.helperApps.neverAsk.saveToDisk','application/octet-stream ,application/zip,application/kswps,application/pdf')  
# 
# #不询问下载路径；后面的参数为要下载页面的Content-type的值
# 
# Content-type请参考网页：http://www.w3school.com.cn/media/media_mimeref.asp
# ————————————————
# 版权声明：本文为CSDN博主「qq_22821275」的原创文章，遵循CC 4.0 BY-SA版权协议，转载请附上原文出处链接及本声明。
# 原文链接：https://blog.csdn.net/qq_22821275/java/article/details/72880323
# 
# 
# # 问题及解决：
# * 中文乱码
# r = requests.get(realurl, timeout=10, headers=headers)
# r.encoding="gb2312"
# 
# * 无法获取动态网页，doc网址
# 安装Gecko driver
# https://github.com/mozilla/geckodriver/releases
# 然后放到python的scripts目录中即可
# li=driver.find_element_by_css_selector("a[onclick^='opendownform']")
# li.click()
# 
# * 关闭单个selenium 页面
# 
# *  如何获取弹出页面
# 用鼠标模拟点击
# 
# 或者用handle 
# handle=browser.current_window_handle #获得当前窗口,也就是弹出的窗口句柄,什么是句柄我也解释不清楚,反正它代表当前窗口
# browser.switch_to_window(handle) #转到当前弹出窗口
# 
# * 关闭窗口
# driver.close()
# 
# * selenium webdriver 右键另存为下载文件（结合robot and autoIt）
# 
# * Firefox无法加载已配置好的Profiles，总是用一个临时文件
# 
# * google driver无法用button.click()，只能用sendkeys('\n'), 而FireFox就可以
# 
# * 网址有中文无法打开，
#  解决：必须用类似'语文'.encode('gb2312')
#  decodedUrl = urllib.parse.quote(('语文').encode('gb2312'))
#  
# * 模式识别抓取某特征字符
# 'https://list.51test.net/w/?nclassid=167&search_key=语文&search_key2=&page=2'
# 中的'语文'要换成%D3%EF%CE%C4
# strSearchKey = re.search('search_key=(.*)&search_key2', NextPageUrl)
# 
# * 判断soup的find为空值
#    if each.find('a') is not None:
#    
# * Dict数组可以作为函数实参进行传递
# 
# * 字典的循环
# for filenumber,filename in dictPageNumberName.items():
#     print( filenumber + " : " + filename)
#     
# * 如何使用不需要打开的chrome，以提高时间，每次只打开一个标签页
# 只要用driver.get(newurl)即可
# 
# * 列出网站地图
# https://www.51test.net/sitemap/ 
# 
# 


# -*- coding: utf-8 -*-
    
import time
import re
import os
import requests
from bs4 import BeautifulSoup
import csv
import math
import json
import urllib

from selenium import webdriver
import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys

from selenium.webdriver.common.action_chains import ActionChains

import re

import socket
import csv
import pandas as pd

from selenium.webdriver.support.ui import Select


######### Chrome Driver

hostname=socket.gethostname()

if hostname=='MyWorkstation':
    userdatadir = "C:/temp/ChromeProfile2" #用于MYWorkStation
    chrome_driver='C:/Users/Aaron/Downloads/chromedriver.exe'
elif hostname=='MyMacWin10':
    userdatadir = "" #用于MyMacwin
elif hostname=="DESKTOP-DEFM935":
    userdatadir = "C:/Users/Administrator/Downloads/51test/GoogleProfile" #用于2570p电脑
    chrome_driver='C:/Users/Administrator/Downloads/chromedriver.exe'
elif hostname=="PLRWORKSTATION":
    userdatadir = "C:/temp/ChromeProfile" #用于PLRWORKSTATION电脑
    chrome_driver='C:/Users/Administrator/AppData/Local/Programs/Python/Python35/chromedriver.exe'


driverOptions = webdriver.ChromeOptions()
driverOptions.add_argument(r"user-data-dir=" + userdatadir)

######### FireFox Driver
hostname=socket.gethostname()
if hostname=='MyWorkstation':
    profileDir = "C:/Users/Aaron/AppData/Roaming/Mozilla/Firefox/Profiles/yn80ouvt.default" #用于MYWorkStation
elif hostname=='MyMacWin10':
    profileDir = "C:/Users/Aaron/AppData/Roaming/Mozilla/Firefox/Profiles/ewg4x7y5.default-release" #用于MyMacwin
elif hostname=="DESKTOP-DEFM935":
    profileDir = "C:\\Users\\Administrator\\Downloads\\51test\\FireFoxProfile" #用于2570p电脑

print(profileDir)
# profile =webdriver.FirefoxProfile(profileDir)

# profile = webdriver.FirefoxProfile()  

profile = webdriver.firefox.firefox_profile.FirefoxProfile(profileDir)


profile.set_preference('browser.download.folderList',2)
profile.set_preference('browser.download.manager.showWhenStarting', True)
profile.set_preference('browser.download.dir','C:\\Users\\Administrator\\Downloads\\51test')
profile.set_preference('browser.helperApps.neverAsk.saveToDisk','application/vnd.openxmlformats-officedocument.wordprocessingml.document,application/msword,application/vnd.ms-word,application/zip,text/plain,application/vnd.ms-excel,text/csv,text/comma-separated-values,application/octet-stream,application/vnd.openxmlformats-officedocument.spreadsheetml.sheet,application/vnd.openxmlformats-officedocument.wordprocessingml.document,application/xml,text/plain,text/xml,text/doc,text/docx,image/jpeg,text/csv,application/octet-stream,text/html,application/x-msdownload,application/zip,application/kswps,application/pdf,application/doc,application/docx')

#### 全部变量

#主题清单地址
# sRealurl='https://www.51test.net/gaokao/manfenzuowen/'
# sRealurl='https://www.51test.net/xsc/yuwen/'
# sRealurl='https://www.51test.net/gaokao/shuxue/shiti/'
# sRealurl='https://www.51test.net/gaokao/jiangsu/shuxue'
sRealurl='https://www.51test.net/xsc/zt/'

#主题页面地址
sTopicPageUrl='https://view.51test.net/docview/?id='

#文件保存地址
sFileSaveFolder="c://"

#页面地址字典，包括编码、主题2个
dictPageNumberName=dict()



headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.13; rv:55.0) Gecko/20100101 Firefox/55.0"}
   

###### 函数 ###### 
#功能：获取网页代码，生成文件名和网页码数组
#输入：经过处理的网页地址
#输出：

def GetPageNumberNameDict(realdict,realurl):
    
    r = requests.get(realurl, timeout=10, headers=headers) #allow_redirects=True

    r.encoding="gb2312"

    soup2=BeautifulSoup(r.text,'lxml')
    # print(r.text)
    tarticles2=soup2.find('div',class_='news-list-left-content').find_all("li")

#     print(tarticles2)

    titlelist=[]
    i=0

    for each in tarticles2:

    #     fullurl='https://www.51test.net' + each.find('a')['href']
    #     fullurl='https://www.51test.net' + each.find('a')['href']

    #     dictPageNumberName[each.find('a')['href'][-12:-5]]=each.find('a').text
        if each.find('a') is not None:
            print(each.find('a')['href'][-13:-5],each.find('a').text)
            realdict[each.find('a')['href'][-13:-5]]=each.find('a').text
        i=i+1




###### 函数 ###### 
#功能：下载文件
#输入：文件代码、文件名称
#输出：保存到本地

def SaveFiles(filenumber, filename):

    
    try:
        # driver=webdriver.Chrome(executable_path=chrome_driver)

        topicurl=sTopicPageUrl + filenumber
        #这个页面是弹出word预览的页面，该页面里包含https://view.51test.net/word/?id=9870584&token=5bfc85dd27e114081435b41830a0fc2e信息

        driver.get(topicurl) # ,allow_redirects=False

        # time.sleep(5)

        ht = driver.page_source

        links_onclick=driver.find_elements_by_css_selector("a[onclick^='opendownform']")
        links_onclick[1].send_keys("\n")

        iframes =driver.find_elements_by_xpath("//iframe")
        # print(len(iframes))
        driver.switch_to.frame(0)

        time.sleep(6)
        # ht=driver.page_source

        # 将selenium找到的页面交给Beautiful Soup分析
        soup = BeautifulSoup(driver.page_source, "lxml")

    #     print(soup)
        address=soup.find('div',class_='regbutton')
#         print(address)

        #动态生成链接的情况  
        if address is None:
            downloadbutton=driver.find_element_by_id('convert')
            downloadbutton.send_keys("\n")

        #有链接的情况    
        else:
            address=soup.find('div',class_='regbutton')

            address=address.find('a')

#             print(address)
#             print(address['href'])

#             print(filename)

            url = address['href']

            urllib.request.urlretrieve(url, sFileSaveFolder + filename + '.doc')

        time.sleep(2)
    except:
        print( '！！错误，无法下载：' + filenumber + ':'+ filename)
    
        #     sFileSaveFolder




###### 函数 ###### 
#功能：转换url中的中文为gb2312编码
#输入：原url
#输出：转换后的url

def GetQuotedPage(oldurl):
        
    strSearchKey = re.search('search_key=(.*)&search_key2', oldurl)
    print(strSearchKey)
    if strSearchKey is not None:
        QuotedSearchKey= urllib.parse.quote((strSearchKey.group(1)).encode('gb2312'))
        print(QuotedSearchKey)
        #替换中文为gb2312代码，生成新网址
        newurl=oldurl.replace(strSearchKey.group(1),QuotedSearchKey)


        strSearchKey2 = re.search('search_key2=(.*)&page', newurl)

        QuotedSearchKey2= urllib.parse.quote((strSearchKey2.group(1)).encode('gb2312'))
        print(QuotedSearchKey2)
        return(newurl.replace(strSearchKey2.group(1),QuotedSearchKey2))
    else:
        return(oldurl)
    



if __name__=="__main__":
    

    # sRealurl=str(input('输入下载地址：'))
    sRealurl='https://www.51test.net/xsc/yuwen'

    r = requests.get(sRealurl, timeout=10, headers=headers,allow_redirects=False)

    r.encoding= "gb2312"

    soup=BeautifulSoup(r.text,'lxml')

    #找到该主题中所有的页面码，如9870581

    tarticles=soup.find_all('li',class_='tuwen')#.find("div").find_all('title')

    titlelist=[]
    i=0

    # print(tarticles[0])
    # fullurl='https://www.51test.net' + tarticles[0].find('a')['href']
    # sTopicName= tarticles[0].find('a').text
    # print(sTopicName)
    # print(fullurl)

    # for each in tarticles:
        
    #     tarticles=soup.find_all('li',class_='tuwen')#.find("div").find_all('title')

    titlelist=[]
    i=0


    #翻页操作
    FirstPageUrl=soup.find('div',class_='showpagelist').find('a')['href']
    # FirstPageUrl='https:' + FirstPageUrl
    FirstPageUrl=FirstPageUrl

    print(FirstPageUrl)

    # search_key和search_key2转为gb2312
    QuotedFirstPageUrl=GetQuotedPage(FirstPageUrl)
    print(QuotedFirstPageUrl)

    #此时还是page2，需要转为page1
    QuotedFirstPageUrl=QuotedFirstPageUrl.replace('page=2','page=1')

    # 如果不增加'&key='，会跳到51test首页，不知什么原因。-210223
    QuotedFirstPageUrl=QuotedFirstPageUrl + '&key='

    #获取第一页的文件数组Dict
    GetPageNumberNameDict(dictPageNumberName,QuotedFirstPageUrl)
    print(dictPageNumberName)

    r = requests.get(QuotedFirstPageUrl, timeout=10, headers=headers,allow_redirects=False)
    r.encoding="gb2312"
    soup2=BeautifulSoup(r.text,'lxml')

    # print(soup2)

    #获取总页数
    iTotalPages=soup2.find('div',class_='list_content_next').text
    iTotalPages =int( re.search('\/(.*)页', iTotalPages).group(1))
    print(iTotalPages)
    QuotedNextPageUrl=QuotedFirstPageUrl.replace('page=1','page=2')

    # for i in range (2,iTotalPages+1):
    for i in range (2,iTotalPages):
        
        GetPageNumberNameDict(dictPageNumberName,QuotedNextPageUrl)
        # print(QuotedNextPageUrl)
        sOldPageNumber='page=' + str(i)
        sNewPageNumber='page=' + str(i+1)
        
        QuotedNextPageUrl=QuotedNextPageUrl.replace(sOldPageNumber,sNewPageNumber)


    #用chrome打开下载页面
    # driver = webdriver.Chrome(executable_path=chrome_driver,options=driverOptions)

    #firefox
    driver = webdriver.Firefox(firefox_profile=profile)
    driver.implicitly_wait(5)

    ##单个测试例
    # SaveFiles('9854593',dictPageNumberName['9854593'])

    for filenumber in dictPageNumberName:
        SaveFiles(filenumber,dictPageNumberName[filenumber])
        time.sleep(2)
        
    driver.close()
    driver.quit()