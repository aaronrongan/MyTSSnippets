
# 目的
- 建立本地A股数据库和zipline的链接，作为一个公共平台
- 对比BackTrader，谁更合适

# 参考文献
- https://www.zipline.io/ 官方教程
- Gitbook出品： 深入了解zipline回测框架 https://rainx.gitbooks.io/-zipline/content/arch/arch.html
- https://pythonprogramming.net/zipline-local-install-python-programming-for-finance/ Sendex的教程
- 開源量化平台zipline之Data Bundles 原文網址：https://kknews.cc/code/bly92l6.html
- https://www.jianshu.com/p/c89a3901d0e8 开源量化平台zipline之Data Bundles
- https://zhuanlan.zhihu.com/p/29850888 zipline的A股改造版本
- https://github.com/zhanghan1990/zipline-chinese zipline A股市场改造。用mogodb、linux系统，有一个虚拟机
- zipline 对于A股改造 https://www.evernote.com/shard/s181/client/snv?noteGuid=26cf9bac-07ec-44c3-bf59-e314f3efe509&noteKey=9bce9b296e224860&sn=https%3A%2F%2Fwww.evernote.com%2Fshard%2Fs181%2Fsh%2F26cf9bac-07ec-44c3-bf59-e314f3efe509%2F9bce9b296e224860&title=zipline%2B%2B%25E5%25AF%25B9%25E4%25BA%258EA%25E8%2582%25A1%25E6%2594%25B9%25E9%2580%25A0 
- zipline 改造 https://stackoverflow.com/questions/25165500/zipline-backtesting-using-non-us-european-intraday-data/25198631#25198631
- 

# 重要文件夹
- C:\Users\Aaron\AppData\Local\Programs\Python\Python35\Scripts\env_zipline\Scripts 
- C:\Users\Aaron\AppData\Local\Programs\Python\Python35\Scripts\env_zipline\Lib\site-packages
- C:\Users\Aaron\.zipline

# 问题
- quandl和quantopian-quandl有什么区别
- 

# 笔记
-  用户可以将任何本地的数据首先转换为DataFrame，其中index按日递增，columns分别为open、high、low、close、volume。然后讲DataFrame作为value，数据ticker为key来构建对应的Panel作为回测本地化的标准数据输入。

- 运行zipline错误，Exception has occurred: JSONDecodeError
解决： https://stackoverflow.com/questions/56957791/getting-jsondecodeerror-expecting-value-line-1-column-1-char-0-with-python （成功。修改benmarks.py/loaders.py,不要用文中提到的第3步）

- bundles/ingest命令

- 用 zipline 1.4有个问题，无法正确显示zipline ingest，报错HDF5之类的，不知什么原因，还是恢复用zipline 1.3.0

- 使用ingest之前，用 set QUANDL_API_KEY=XNUFNU1MtPH-hd8rMdGs 

- 有2种数据bundle，一种是新建一个，一种是用csvdir bundle

## 常用命令
- 

## 如何注册一个新bundle
- 有了正確格式的csv文件後，需要修改~/.zipline/extension.py，同時需要引入csvdir與pandas。原文網址：https://kknews.cc/code/bly92l6.html
- 注册一个新bundles,使用register()註冊該bundle 原文網址：https://kknews.cc/code/bly92l6.html
- 需要新建一个TradingCalendars，不同于美股 https://www.zipline.io/trading-calendars.html#building-a-custom-trading-calendar 
新建中国沪指股市日历，见C:\Users\Aaron\AppData\Local\Programs\Python\Python35\Scripts\env_zipline\Lib\site-packages\trading_calendars\trading_calendar.py
class CSSExchangeCalendar(TradingCalendar):
- 

## zipline修改文件清单
- benchmarks.py
- trading.py
- trading_calendar.py
- （~/.zipline/extension.py) 