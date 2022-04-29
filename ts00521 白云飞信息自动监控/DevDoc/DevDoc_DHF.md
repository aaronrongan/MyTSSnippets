# DHF 抓取白云飞网络策略 


## 目的
* 抓取白云飞网页，获取实时持仓变动信息，发送给短信、邮件，及时调仓
* 

## 要点
* D  beautifulsoup解析网页
* D  发送电话消息用twillo 
* D 清除刷新output: cmd用sys.stdout.flush()；Jupyter用from IPython.display import clear_output；对于单行模式，可以用'\r...'
* D 存为bat执行,注意要用ANSI格式保存，
* D 如何实现用post登陆网页，得到新cookies，然后爬取新的网页，用以下网页
    * r = s.post(postUrl, data=PayloadData, headers=payloadHeader)
    * 新做法：绕过cookies，直接用http://17fx.net/F2020/login.aspx?refurl=http%3a%2f%2f17fx.net%2fF2020%2fb_follow.aspx 网址+postdata来登陆
* D 清除屏幕 clear_output()用于Jupyter 或 os.system('cls') 用于command模式
* 使用Selenium抓取网页

## 后续
* 对一个组合进行抓取
* cookies如何动态更新？否则不实用。（错误：关键在于时间戳的转换，里面的1581..其实当时的时间，应该就是换上当时的时间即可）https://tool.lu/timestamp/ 这是时间戳显示工具
* 已有仓位如何保留在本地，免得每次启动都要发送一次短信？比较日期是否是今天？本日的第一次启动需要对比，后面都已通过看手机知道

# Learning Points