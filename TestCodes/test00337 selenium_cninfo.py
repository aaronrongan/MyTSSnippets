# -*- coding:utf-8 -*-

#Ŀ��:
###190925   ��selenium�򿪣�Ȼ��ץȡ��ҳ�е���Ϣ����Ʊ���ַ
##191204    ��Ҫ��װgeckodriver

#Ҫ��   
#1. 2�μ��sleep
#2. ����������ҳ
#    ht = driver.page_source
#   ht=ht.encode('gb18030').decode('gb18030')
#3. ���ݽ�����BeautifulSoupʵ�֣��õ�find/find all�Լ�html�����е�td/table��Ԫ��
#4. ��ҳ��ҳʵ�֣��ҵ�Ԫ�أ�Ȼ��action...arrow_down
#5. pandas dataframe�Ĵ���

#BUG��
# 1. �߼������⣬ѭ�������һҳû��ץȡ����

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
# wait = WebDriverWait(browser,10)#ָ����ȴ�ʱ��
#����ȴ�����presence_of_element_located������ڵ���֣������ǽڵ�Ķ�λԪ��IDΪq��������#
# 10�������IDΪq�Ľڵ�ɹ����س����ͷ��ظýڵ�
# input = wait.until(EC.presence_of_element_located((By.ID,'q')))
# #���ڰ�ť���򽫵ȴ���������Ϊelement_to_be_clickable��ʾ�ɵ�������10���ڿɵ���ͷ��������ť�ڵ�
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
    profileDir = "C:/Users/Aaron/AppData/Roaming/Mozilla/Firefox/Profiles/yn80ouvt.default" #����MYWorkStation
elif hostname=='MyMacWin10':
    profileDir = "C:/Users/Aaron/AppData/Roaming/Mozilla/Firefox/Profiles/ewg4x7y5.default-release" #����MyMacwin
elif hostname=="DESKTOP-DEFM935":
    a=1
    

profile =webdriver.FirefoxProfile(profileDir)
driver = webdriver.Firefox(profile)
driver.implicitly_wait(5)

# base_url = "www.baidu.com"cls
# driver=webdriver.Firefox()

# driver.get('https://www.lixinger.com/analytics/company/sz/300383/detail/announcement?type=all&page-index=0/') #���еĹ���
# driver.get('https://www.lixinger.com/analytics/company/sz/000001/detail/announcement?type=fs&page-index=0') #�Ʊ�
# driver.get('http://webapi.cninfo.com.cn/#/thematicStatistics')

# driver.get('http://webapi.cninfo.com.cn/api/sysapi/p_sysapi1024?tdate=2019-12-10')

driver.get('http://webapi.cninfo.com.cn/#/thematicStatistics?id=538')

#ҵ�������������, ������ʾδ��Ȩ
# driver.get('http://webapi.cninfo.com.cn/api/sysapi/p_sysapi1066?apiname=p_sysapi1040')

# buyers=driver.find_elements_by_xpath('//div[@title=����]')
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
# a = driver.find_element_by_link_text('��һҳ')
# a.click()

#################################
# CompanyAddress = soup.find('table', id="contentTable").find_all('a')
# for each in CompanyAddress:
#     print(each.get('href'))
################################    

###���ﻹҪ����һ�����ͷ��ץȡԪ�ض�Ӧ�ı�ͷ�ֶ�

##########�ҵ����ͷ
thead=soup.find('thead').find_all('th')#.find("div").find_all('title')
# for each in thead:
#     print(each.find("div").text)

    # print('\n')

############�ҵ�һ������ҳ
pagelast=driver.find_element_by_xpath("//li[@class='page-last']/a")
totalpages=int(pagelast.text)

##############ѭ�����totalpages-1��
# for each in totalpages-1:
companylist=[]

for _ in range(0,9):
    
    ##########�ҵ�����Ԫ��
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
    #�ҵ���һҳ��λ�ã�ע��Ҫ��a href����ط���������һ��
    pagenextxpath=driver.find_element_by_xpath("//li[@class='page-next']/a")
    # print(pagenextxpath.text)
    
    
    #######################################################
    #����ƶ��ҵ���һҳ��λ�ã�Ȼ����
    action=ActionChains(driver).move_to_element(pagenextxpath)
    action.click().perform() 
    time.sleep(2)
    #########��һ��ץȡ��ҳ
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
#���������������ַ���
# inputbox.clear
# inputbox.send_keys(Keys.ARROW_DOWN) 
# inputbox.send_keys("300383") 
# inputbox.send_keys(Keys.RETURN)
#######################################

# action.context_click(pagenext)
# pagenext.send_keys(Keys.RETURN) 