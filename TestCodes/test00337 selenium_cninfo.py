# -*- coding:utf-8 -*-

#目的:
###190925   用selenium打开，然后抓取网页中的信息，如财报地址
##191204    需要安装geckodriver

#要点   
#1. 2次间隔sleep
#2. 解码中文网页
#    ht = driver.page_source
#   ht=ht.encode('gb18030').decode('gb18030')
#3. 内容解析用BeautifulSoup实现，用到find/find all以及html语言中的td/table等元素
#4. 网页翻页实现：找到元素，然后action...arrow_down
#5. pandas dataframe的创建

#BUG：
# 1. 逻辑有问题，循环到最后一页没有抓取数据

import requests
import unittest
from bs4 import BeautifulSoup

import urllib3
from selenium import webdriver
import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys

from selenium.webdriver.common.action_chains import ActionChains

import socket



# browser = webdriver.Chrome()
# browser.get('https://www.taobao.com/')
# wait = WebDriverWait(browser,10)#指定最长等待时间
#传入等待条件presence_of_element_located，代表节点出现，参数是节点的定位元组ID为q的搜索框#
# 10秒内如果ID为q的节点成功加载出来就返回该节点
# input = wait.until(EC.presence_of_element_located((By.ID,'q')))
# #对于按钮，则将等待条件更改为element_to_be_clickable表示可点击，如果10秒内可点击就返回这个按钮节点
# button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR,'.btn-search')))
# print(input,button)



# import TimeUnit

# class Register(unittest.TestCase):
# 	def setUp(self):
# 		self.profileDir = "C:/Users/Administrator/AppData/Roaming/Mozilla/Firefox/Profiles/xngshdad.Python"
# 		self.profile = webdriver.FirefoxProfile(self.profileDir)
# 		self.driver = webdriver.Firefox(self.profile)
# 		self.driver.implicitly_wait(30)
# 		self.base_url = "www.baidu.com"
# 		self.verificationErrors = []

# profileDir = "C:/Users/Administrator/AppData/Roaming/Mozilla/Firefox/Profiles/3n0dd184.default-release"
# 

hostname=socket.gethostname()
if hostname=='MyWorkstation':
    profileDir = "C:/Users/Aaron/AppData/Roaming/Mozilla/Firefox/Profiles/yn80ouvt.default" #用于MYWorkStation
elif hostname=='MyMacWin10':
    profileDir = "C:/Users/Aaron/AppData/Roaming/Mozilla/Firefox/Profiles/ewg4x7y5.default-release" #用于MyMacwin
elif hostname=="DESKTOP-DEFM935":
    a=1
    

profile =webdriver.FirefoxProfile(profileDir)
driver = webdriver.Firefox(profile)
driver.implicitly_wait(5)

# base_url = "www.baidu.com"cls
# driver=webdriver.Firefox()

# driver.get('https://www.lixinger.com/analytics/company/sz/300383/detail/announcement?type=all&page-index=0/') #所有的公告
# driver.get('https://www.lixinger.com/analytics/company/sz/000001/detail/announcement?type=fs&page-index=0') #财报
# driver.get('http://webapi.cninfo.com.cn/#/thematicStatistics')

# driver.get('http://webapi.cninfo.com.cn/api/sysapi/p_sysapi1024?tdate=2019-12-10')

driver.get('http://webapi.cninfo.com.cn/#/thematicStatistics?id=538')

#业绩大幅上升链接, 但是显示未授权
# driver.get('http://webapi.cninfo.com.cn/api/sysapi/p_sysapi1066?apiname=p_sysapi1040')

# buyers=driver.find_elements_by_xpath('//div[@title=“”]')
# elements=driver.find_elements_by_xpath('//div[1]/div/div/div[3]')

# elements=driver.find_elements_by_xpath('//div[@class="table-container"]')

# print(elements[0].getdis)

# ht = driver.page_source
# ht = driver.page_source
# print(ht)
# print(elements[0]])

# soup = BeautifulSoup(ht,'html.parser')
# WebDriverWait(driver,30)

# 
time.sleep(5)

ht = driver.page_source
ht=ht.encode('gb18030').decode('gb18030')
# ht=ht.encode("raw_unicode_escape")

#print(ht)
# print(ht.)

# print(ht.encode('utf-8'))
# print(ht.encode('gb18030').encode("raw_unicode_escape").decode("utf-8"))

soup =BeautifulSoup(ht, 'lxml')
# print(soup)
# a = driver.find_element_by_link_text('下一页')
# a.click()

#################################
# CompanyAddress = soup.find('table', id="contentTable").find_all('a')
# for each in CompanyAddress:
#     print(each.get('href'))
################################    

###这里还要建立一个表格头，抓取元素对应的表头字段

##########找到表格头
thead=soup.find('thead').find_all('th')#.find("div").find_all('title')
# for each in thead:
#     print(each.find("div").text)

    # print('\n')

############找到一共多少页
pagelast=driver.find_element_by_xpath("//li[@class='page-last']/a")
totalpages=int(pagelast.text)

##############循环点击totalpages-1次
# for each in totalpages-1:
companylist=[]

for _ in range(0,9):
    
    ##########找到各个元素
    trs=soup.find('table', id="contentTable").find('tbody').find_all('tr')
    for each in trs:
#         print(each)
        companylist.append(each.find_all('a')[1].text)
#         print(each.find_all('a')[1].text)
#         print('\n')
    
    #########
    # pagenext=driver.find_element_by_class_name("page-next")

    # inputbox=driver.find_element_by_id("search-input")

    # pagenextxpath=driver.find_element_by_xpath("/html/body/div/div[0]/div")
    #######################################################
    #找到下一页的位置，注意要到a href这个地方，不是上一级
    pagenextxpath=driver.find_element_by_xpath("//li[@class='page-next']/a")
    # print(pagenextxpath.text)
    
    
    #######################################################
    #鼠标移动找到下一页的位置，然后点击
    action=ActionChains(driver).move_to_element(pagenextxpath)
    action.click().perform() 
    time.sleep(2)
    #########再一次抓取网页
    ht = driver.page_source
    ht=ht.encode('gb18030').decode('gb18030')
    # ht=ht.encode("raw_unicode_escape")

    #print(ht)
    # print(ht.)

    # print(ht.encode('utf-8'))
    # print(ht.encode('gb18030').encode("raw_unicode_escape").decode("utf-8"))

    soup =BeautifulSoup(ht, 'lxml')
#     print(soup)
print(companylist)



# action.context_click().perform() 
# action.send_keys(Keys.ARROW_DOWN) 

# ActionChains(driver).move(1592, 756).click().perform() 
# ActionChains(driver).move(1592, 756).context_click().perform()
# time.sleep(3) 

# action2=ActionChains(driver).move_to_element(inputbox)
# action2.send_keys(Keys.ARROW_DOWN) 
# action2.send_keys("300383") 
# action2.send_keys(Keys.RETURN) 
# time.sleep(3) 

########################################
#在搜索框中搜索字符串
# inputbox.clear
# inputbox.send_keys(Keys.ARROW_DOWN) 
# inputbox.send_keys("300383") 
# inputbox.send_keys(Keys.RETURN)
#######################################

# action.context_click(pagenext)
# pagenext.send_keys(Keys.RETURN) 