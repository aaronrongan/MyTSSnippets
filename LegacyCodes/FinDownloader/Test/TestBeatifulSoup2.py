# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
import requests
import socket
from urllib import  request

socket.setdefaulttimeout(10)

# headers1={"User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10.13; rv:55.0) Gecko/20100101 Firefox/55.0"}
send_headers = {
                'Accept-Encoding':'gzip, deflate, br',
                'Sec-Fetch-Site':'same-origin',
                'Host':'www.lixinger.com',
                'Cache-Control':'max-age=0',
                # 'Cookie':'Hm_lvt_ec0ee7e5c8bed46d4fdf3f338afc08f5=1569491782; Hm_lpvt_ec0ee7e5c8bed46d4fdf3f338afc08f5=1569491782; jwt=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJfaWQiOiI1Yjc5Mjc5YmQ0M2I5MjEwMjAxNDJhZmUiLCJpYXQiOjE1Njk0OTE3OTgsImV4cCI6MTU3MDA5NjU5OH0.F8KV_PGvBYg4bpny3x5_a_J5UJhYYjdBObwTgfhYbZM',
                # 'Cookie':,

                'ETag': 'W / "9d6-ur/uBzgatny2qgtgjuC5lXpxU4w"',
                'Sec-Fetch-Mode':'navigate',
                'Sec-Fetch-User':'?1',
                'Upgrade-Insecure-Requests':'1',
                'Referer':'https://www.lixinger.com/analytics/company/sz/300383/detail/announcement?type=fs&page-index=0',
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) \
                Chrome/77.0.3865.75 Safari/537.36",
                "Connection": "keep-alive",
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
                "Accept-Language": "zh-CN,zh;q=0.9"    }

send_headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'}

# url='http://vip.stock.finance.sina.com.cn/corp/go.php/vCB_Bulletin/stockid/002271/page_type/ndbg.phtml'
url='https://www.lixinger.com/analytics/company/sz/300383/detail/announcement?announcement-type=fs&page-index=0'
# url='https://www.lixinger.com/profile/center/home/all'
# url='http://blog.csdn.net/beliefer/article/details/51251757'
r = requests.get(url, headers=send_headers)
# r.encoding='gbk'
# r.close()

# req = request.Request(url, headers = send_headers)
# text = request.urlopen(req).read().decode()
# print(text)

print(r.text)
# source=requests.get('https://www.lixinger.com/analytics/company/sz/300383/detail/announcement?announcement-type=fs&page-index=0').text

# source=requests.get('http://vip.stock.finance.sina.com.cn/corp/go.php/vCB_Bulletin/stockid/002271/page_type/ndbg.phtml').text

# soup=BeautifulSoup(r.text,'lxml')

# print(soup.prettify())
# print(soup.find('div',class_='tui').h2)








