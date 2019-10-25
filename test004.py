
###190925 用selenium抓取网页
import requests

import urllib3
from selenium import webdriver

driver=webdriver.Firefox()
driver.get('https://www.lixinger.com/analytics/company/sz/300012/detail/announcement?type=all&page-index=0/')
print(driver)