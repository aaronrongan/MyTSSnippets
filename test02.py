import sys
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

url="https://www.lixinger.com/analytics/company/sz/300012/detail/announcement?type=all&page-index=0"
client_response=Client(url)
source=client_response.mainFrame().toHtml()