
import wget
import urllib.request

url='http://static.cninfo.com.cn/finalpage/2019-08-16/1206532802.PDF'

wget.download(url,'../../../1206532802.pdf')
# 或者
urllib.request.urlretrieve(url,filename="../../../1206532802.pdf")