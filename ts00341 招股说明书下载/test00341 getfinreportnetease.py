# https://zhuanlan.zhihu.com/p/44753154

# python爬取A股财务报表（含代码）]

# 可用。lrb就是利润表

# 量化交易除了在K线上可以有所应用，还可以用于基本面的操作，在处理数据之前首先要获取数据，网易财经给我们提供了一个方便的API接口，这样就不必在巨潮资讯网里面使用收钱的API（大家快给我打赏啊！）

import re,urllib
import xlwt
from bs4 import BeautifulSoup
from time import sleep

count = 1
for count in range(600500,600600):
    url = 'http://quotes.money.163.com/service/lrb_'+str(count)+'.html'
    while True:
        try:
            content = urllib.request.urlopen(url,timeout=2).read()
            print(content)
            with open('../利润表/'+str(count)+'lrb.csv','wb') as f:
                f.write(content)
            print(count)
            sleep(1)
            break
        except Exception as e:
            if str(e) =='HTTP Error 404: Not Found':
                break
            else:
                print(e)
                continue