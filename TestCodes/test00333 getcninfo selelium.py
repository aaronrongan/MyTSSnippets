#�?��:
###190925   用selenium打开，然后抓取网页中的信�?��如财报地址
##191204    需要安装geckodriver
#要点   2次间隔sleep


#-*- coding:utf-8 -*-
import requests
import unittest

import urllib3
from selenium import webdriver
import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# browser = webdriver.Chrome()
# browser.get('https://www.taobao.com/')
# wait = WebDriverWait(browser,10)#指定最长等待时�?
#传入等待条件presence_of_element_located，代表节点出现，参数�?��点的定位元组ID为q的搜索�?#
# 10秒内如果ID为q的节点成功加载出来就返回该节�?
# input = wait.until(EC.presence_of_element_located((By.ID,'q')))
# #对于按钮，则将等待条件更改为element_to_be_clickable表示�?��击，如果10秒内�?��击就返回这个按钮节点
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
# profileDir = "C:/Users/Aaron/AppData/Roaming/Mozilla/Firefox/Profiles/yn80ouvt.default" #用于MYWorkStation
profileDir = "C:/Users/Aaron/AppData/Roaming/Mozilla/Firefox/Profiles/ewg4x7y5.default-release" #用于MyMacwin
profile =webdriver.FirefoxProfile(profileDir)
driver = webdriver.Firefox(profile)
driver.implicitly_wait(30)
# base_url = "www.baidu.com"cls
# driver=webdriver.Firefox()

# driver.get('https://www.lixinger.com/analytics/company/sz/300383/detail/announcement?type=all&page-index=0/') #所有的�?��
# driver.get('https://www.lixinger.com/analytics/company/sz/000001/detail/announcement?type=fs&page-index=0') #财报
# driver.get('http://webapi.cninfo.com.cn/#/thematicStatistics')

# driver.get('http://webapi.cninfo.com.cn/api/sysapi/p_sysapi1024?tdate=2019-12-10')

driver.get('http://webapi.cninfo.com.cn/#/thematicStatistics?id=538')

#业绩大幅上升链接, 显示�?���?
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

print(ht.encode('utf-8'))

# driver.quit()