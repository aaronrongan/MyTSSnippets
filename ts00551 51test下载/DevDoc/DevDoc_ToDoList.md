

## 目的：
下载51test等网站的word考试卷、辅导材料等

## 参考资料：
https://www.51test.net/
cninfo巨潮网下载年报
0daydownscrap

## 重点：
翻页
BeautifulSoup
requests

* Firefox driver的设置

profile = webdriver.firefox.firefox_profile.FirefoxProfile(profileDir)


profile.set_preference('browser.download.folderList',2)
profile.set_preference('browser.download.manager.showWhenStarting', True)
profile.set_preference('browser.download.dir','C:\\Users\\Administrator\\Downloads\\51test')
profile.set_preference('browser.helperApps.neverAsk.saveToDisk','application/vnd.openxmlformats-officedocument.wordprocessingml.document,application/msword,application/vnd.ms-word,application/zip,text/plain,application/vnd.ms-excel,text/csv,text/comma-separated-values,application/octet-stream,application/vnd.openxmlformats-officedocument.spreadsheetml.sheet,application/vnd.openxmlformats-officedocument.wordprocessingml.document,application/xml,text/plain,text/xml,text/doc,text/docx,image/jpeg,text/csv,application/octet-stream,text/html,application/x-msdownload,application/zip,application/kswps,application/pdf,application/doc,application/docx')

profile.set_preference("browser.altClickSave", True)
profile.update_preferences()

driver = webdriver.Firefox(firefox_profile=profile)

* chrome driver的设置
driverOptions = webdriver.ChromeOptions()
driverOptions.add_argument(r"user-data-dir=C:\Users\Administrator\Downloads\51test\GoogleProfile")
chrome_driver='C:/Users/Administrator/Downloads/chromedriver.exe'

driver = webdriver.Chrome(executable_path=chrome_driver,options=driverOptions)

* 找到弹出的页面
其实是一个frame
iframes =driver.find_elements_by_xpath("//iframe")
print(len(iframes))
driver.switch_to.frame(0)

* 将selenium找到的页面交给Beautiful Soup分析
soup = BeautifulSoup(driver.page_source, "lxml")

* 网页文件有2种形式，一种是已经生成的，一种是需要现场convert的；
前者需要用beautifulsoup获取地址即可
后者需要用selenium获取按钮，然后

## 算法：
1. 配置Chrome driver

2. 给定一个网页链接，比如“高考满分作文”，下载该专题
https://www.51test.net/gaokao/manfenzuowen/

3. 遍历获取每个文件的链接页面，如https://www.51test.net/show/9870584.html，获得ID号码

4. 获取下载页面
https://user.51test.net/vip/download/word/?id=9870584

预览的页面为：
url='https://view.51test.net/docview/?id=9870584' #这个页面是弹出word预览的页面，该页面里包含https://view.51test.net/word/?id=9870584&token=5bfc85dd27e114081435b41830a0fc2e信息

5. 实际的页面有2种，一个是静态地址，一个是动态地址


## 流程
分析版面页面，抓取实际链接
|
获取所有页面从1~13页的链接，进行searchkey的中文处理
|
对每个页面进行分析，获取dict，文件编码和文件名称
|
进入下载页面，弹出页面
|
下载文件，保存
|
进行下一个页面的分析

## 进阶：
一次性爬取所有试卷信息
============================
通过修改Firefox设置配置下载不做选择，直接下载到某个目录

http://www.mamicode.com/info-detail-1283143.html
https://blog.csdn.net/qq_22821275/article/details/72880323

第二步：修改Firefox的相关配置。

profile.set_preference('browser.download.folderList',2)    

#设置成0代表下载到浏览器默认下载路径；设置成2则可以保存到指定目录

profile.set_preference('browser.download.dir','F:\\Users')  

#保存到指定目录F盘Users文件夹。可以任意文件夹，但是记得分隔符是两个反斜杠

profile.set_preference('browser.download.manager.showWhenStarting',False)

#不管是True还是False，都不显示开始，直接开始下载

profile.set_preference('browser.helperApps.neverAsk.saveToDisk','application/octet-stream ,application/zip,application/kswps,application/pdf')  

#不询问下载路径；后面的参数为要下载页面的Content-type的值

Content-type请参考网页：http://www.w3school.com.cn/media/media_mimeref.asp
————————————————
版权声明：本文为CSDN博主「qq_22821275」的原创文章，遵循CC 4.0 BY-SA版权协议，转载请附上原文出处链接及本声明。
原文链接：https://blog.csdn.net/qq_22821275/java/article/details/72880323


# 问题及解决：
* 中文乱码
r = requests.get(realurl, timeout=10, headers=headers)
r.encoding="gb2312"

* 无法获取动态网页，doc网址
安装Gecko driver
https://github.com/mozilla/geckodriver/releases
然后放到python的scripts目录中即可
li=driver.find_element_by_css_selector("a[onclick^='opendownform']")
li.click()

* 关闭单个selenium 页面

*  如何获取弹出页面
用鼠标模拟点击

或者用handle 
handle=browser.current_window_handle #获得当前窗口,也就是弹出的窗口句柄,什么是句柄我也解释不清楚,反正它代表当前窗口
browser.switch_to_window(handle) #转到当前弹出窗口

* 关闭窗口
driver.close()

* selenium webdriver 右键另存为下载文件（结合robot and autoIt）

* Firefox无法加载已配置好的Profiles，总是用一个临时文件

* google driver无法用button.click()，只能用sendkeys('\n'), 而FireFox就可以

* 网址有中文无法打开，
 解决：必须用类似'语文'.encode('gb2312')
 decodedUrl = urllib.parse.quote(('语文').encode('gb2312'))
 
* 模式识别抓取某特征字符
'https://list.51test.net/w/?nclassid=167&search_key=语文&search_key2=&page=2'
中的'语文'要换成%D3%EF%CE%C4
strSearchKey = re.search('search_key=(.*)&search_key2', NextPageUrl)

* 判断soup的find为空值
   if each.find('a') is not None:
   
* Dict数组可以作为函数实参进行传递

* 字典的循环
for filenumber,filename in dictPageNumberName.items():
    print( filenumber + " : " + filename)
    
* 如何使用不需要打开的chrome，以提高时间，每次只打开一个标签页
只要用driver.get(newurl)即可

* 列出网站地图
https://www.51test.net/sitemap/ 