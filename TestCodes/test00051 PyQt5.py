##目的: 范例：用PyQt5爬虫

import sys

import bs4 as bs

import urllib.request

from PyQt5.QtWebKitWidgets import QWebPage

from PyQt5.QtWebKitWidgets import QWebView

from PyQt5.QtWidgets import QApplication

from PyQt5.QtCore import QUrl



class Client(QWebPage):

    

    def _init_ (self, url):

        self.app = QApplication(sys.argv)

        QWebPage.__init__(self)

        self.loadFinished.connect(self.on_page_load)

        self.mainFrame().load(QUrl(url))

        self.app.exec()

    

    def on_page_load(self):

        self.app.quit()

        

url = 'https://pythonprogramming.net/parsememcparseface/'

client_response = Client(url)

source = client_response.mainFrame().toHtml()



soup = bs.BeautifulSoup(source, 'lxml')

js_test = soup.find('p', class_ = 'jstest')

print(js_test.text)