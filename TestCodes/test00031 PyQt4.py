
#目的:
###191024 用PyQt4模组来抓取后续动态需要的网页，其实是伪造一个浏览器的方式

#问题：无法import sip
#解决：换用了PLRWorkstation anaconda就可以了
#需要安装PyQt4，wheel文件，在Anaconda的Python下安装
#https://pythonprogramming.net

import requests
import sys
import sip
import PyQt5.QtGui

from PyQt5.QtGui import QApplication
from PyQt5.QtCore import QUrl
from PyQt5.QtWebKit import QWebPage

from PyQt4.QtGui import QApplication
from PyQt4.QtCore import QUrl
from PyQt4.QtWebKit import QWebPage


import bs4 as bs
import urllib.request
	

class Client(QWebPage):

	def _init_ (self, url):
		self.app=QApplication(sys.argv)
		QWebPage._init_(self)
		self.loadFinished.connect(self.on_page_load)
		self.mainFrame().load(QUrl(url))
		self.app.exec_()

	def on_page_load(self):
		self.app.quit()

url='https://www.lixinger.com/analytics/company/sz/300012/detail/announcement?type=all&page-index=0/'
url='https://pythonprogramming.net/parsememcparseface/'
Client()
client_response=Client(url)
source=client_response.mainFrame().toHtml()

print(source)
source=urllib.request.urlopen(‘https...”)
soup=bs.BeautifulSoup(source, ‘lxml’)
js_test=soup.find(‘p’,class_=‘jstest’)

print(js_test.text)	