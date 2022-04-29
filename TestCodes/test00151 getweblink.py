

# -*- coding: utf-8 -*-

#读取html文件

import re
import requests
from bs4 import BeautifulSoup

headers1={"User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10.13; rv:55.0) Gecko/20100101 Firefox/55.0"}
send_headers = {    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36",    "Connection": "keep-alive",    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",    "Accept-Language": "zh-CN,zh;q=0.8"    }

r = requests.get('https://www.lixinger.com/analytics/company/sz/300383/detail/announcement?announcement-type=fs&page-index=0',timeout=10,headers=send_headers)
r.close()

print(r.encoding)

soup=BeautifulSoup(r,'lxml')

print(soup.prettify())
# print(r.headers)

# print(r.json())

#PageUrl="https://www.lixinger.com/analytics/company/sz/300383/detail/announcement?announcement-type=fs&page-index=0"

#file_url = re.search('http://file.finance.sina.com.cn/211.154.219.97:9494/.*?PDF',PageUrl)