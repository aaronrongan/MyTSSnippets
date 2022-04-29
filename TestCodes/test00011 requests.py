
# 目的: 
#1.使用Requests+header方式获取网页内容
#2. 

import requests

###191023 直接抓取页面显示“你的浏览器不支持，原因在于网页是动态加载需要的页面
# re= requests.get("https://www.lixinger.com/analytics/company/sz/300012/detail/announcement?type=all&page-index=0")
# print(re.text)

# headers={
	# "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
	# "Accept-Encoding":"gzip, deflate, br",
	# "Accept-Language":"zh-CN,zh;q=0.9,en;q=0.8",
	# "Connection":"keep-alive",
	# "Cookie":"TYCID=95527c1610397911e8bff6ed77ba820561; undefined=527c1610397911e8bff6ed77ba820561; ssuid=1836004500; _ga=GA1.2.1102138489.1531815381; _gid=GA1.2.439505005.1543210985; tyc-user-info=%257B%2522myQuestionCount%2522%253A%25220%2522%252C%2522integrity%2522%253A%25220%2525%2522%252C%2522state%2522%253A%25220%2522%252C%2522vipManager%2522%253A%25220%2522%252C%2522onum%2522%253A%25220%2522%252C%2522monitorUnreadCount%2522%253A%252231%2522%252C%2522discussCommendCount%2522%253A%25221%2522%252C%2522token%2522%253A%2522eyJhbGciOiJIUzUxMiJ9.eyJzdWIiOiIxMzcyNTUwNTc2OCIsImlhdCI6MTU0MzMwODIwMiwiZXhwIjoxNTU4ODYwMjAyfQ.Lv41AYfYcieyjXObqukIfhuzFDa_H2Vb3Xuh7MqHDn9wHKpQG87X02yRJ2LB3MS2R-vr5Yn2AogHvnwHxHtxPQ%2522%252C%2522redPoint%2522%253A%25220%2522%252C%2522pleaseAnswerCount%2522%253A%25221%2522%252C%2522vnum%2522%253A%25220%2522%252C%2522bizCardUnread%2522%253A%25220%2522%252C%2522mobile%2522%253A%252213725505768%2522%257D; auth_token=eyJhbGciOiJIUzUxMiJ9.eyJzdWIiOiIxMzcyNTUwNTc2OCIsImlhdCI6MTU0MzMwODIwMiwiZXhwIjoxNTU4ODYwMjAyfQ.Lv41AYfYcieyjXObqukIfhuzFDa_H2Vb3Xuh7MqHDn9wHKpQG87X02yRJ2LB3MS2R-vr5Yn2AogHvnwHxHtxPQ; RTYCID=51b3ced1f28d4882a3978233b80680d3; CT_TYCID=a3fc8e61319e4802a17aa906f3b3b0da; aliyungf_tc=AQAAAEvHyG+iwwAA+Olw3P3xcz7pHmCO; csrfToken=OZverume68dXtF1ctYCNRzO5; Hm_lvt_e92c8d65d92d534b0fc290df538b4758=1543310105,1543385226,1543390158,1543398990; Hm_lpvt_e92c8d65d92d534b0fc290df538b4758=1543399314",
	# "Host":"www.tianyancha.com",
	# "Upgrade-Insecure-Requests":"1",
	# "User-Agent":"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36"
# }
 
# send_headers = {
# "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36 Edge/18.18362", 
# "Connection": "keep-alive",
# "Cache-Control": "max-age=0",
# "Origin": "https://www.lixinger.com",
# "Accept-Encoding": "gzip, deflate, br",
# "Cookies":"Hm_lpvt_ec0ee7e5c8bed46d4fdf3f338afc08f5=1571926341; jwt=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJfaWQiOiI1Yjc5Mjc5YmQ0M2I5MjEwMjAxNDJhZmUiLCJpYXQiOjE1NzE5MjYzMTQsImV4cCI6MTU3MjUzMTExNH0.o5bXRjtUb9vdIIR2W93AvcGfpeG7nGi45rUKDEpFI2Y; Hm_lvt_ec0ee7e5c8bed46d4fdf3f338afc08f5=1570710326,1570721805,1570800043,1571660830", 
# "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
# "Accept-Language": "zh-CN,zh;q=0.8"}

send_headers = {
"Accept": "application/json, text/plain, */*",
"Accept-Encoding": "gzip, deflate, br",
"Accept-Language": "en-US, en; q=0.8, zh-Hans-CN; q=0.5, zh-Hans; q=0.3",
"Cache-Control": "max-age=0",
"Connection": "Keep-Alive",
"Content-Length": "64",
"Content-Type": "application/json; charset=utf-8",
"Cookie": "Hm_lpvt_ec0ee7e5c8bed46d4fdf3f338afc08f5=1571926341; jwt=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJfaWQiOiI1Yjc5Mjc5YmQ0M2I5MjEwMjAxNDJhZmUiLCJpYXQiOjE1NzE5MjYzMTQsImV4cCI6MTU3MjUzMTExNH0.o5bXRjtUb9vdIIR2W93AvcGfpeG7nGi45rUKDEpFI2Y; Hm_lvt_ec0ee7e5c8bed46d4fdf3f338afc08f5=1570710326,1570721805,1570800043,1571660830",
"Host": "www.lixinger.com",
"Origin": "https://www.lixinger.com",
"Referer": "https://www.lixinger.com/analytics/company/sh/600009/detail/announcement?type=fsfc&page-index=0",
"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36 Edge/18.18362"
}

realurl="https://www.lixinger.com/api/stock/posts/announcement/list"
# re= requests.get(realurl)
re=requests.get(realurl, timeout=10, headers=send_headers)
print(re)
