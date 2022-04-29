# 设计文档：
================
ts00571 动量轮动策略获取信号，一种趋势交易

[toc]

# 目的
- 获取指数、ETF涨幅和均线差值数值,为ts00571做测试，按ts00571.xlsx来
- 因为Excel获取Choice的方式非常慢，做测试可以，但是实时太慢。
- 利用TuShare、JQData库，后面可以尝试聚宽库
- 功能：
  - 单次交互查询
  - 实时监控发送信号
  - 回测
  - 多次回测，对参数进行优化

- 将几个ETF趋势动量策略用自己的代码实现，能够发送实时提醒，比如手机、微信

- 先用ipynb实现，然后放到服务器上实现

# 总结(20.08.11)
- 7-15~8-11，基本完成计划的功能：查询、提醒、单次回测、多次优化；

- Python功力提到很大提高，类的使用，抽象类、复用类

- 建立数据库

- 超过一半时间在纠错，很多小错误

- 牺牲了陪伴家人的时间、工作时间

- 策略不够灵活，没有达到zipline/quantopian/聚宽那种模式写一个策略就能用

- 动量轮动策略的参数还是没有找到规律，选择偶然性很大，并不是百战不败的工具。还是要想法找到一个方向

- 看来还是要有一个回测框架，把精力放在策略上，而不是都用来解决bug

- 这个策略的最大优点应该是即便不好的参数，也很难发生大幅亏损的情况

- 从测试结果看，胜率其实大部分都是在50%左右摆动，这个策略的优点就是小亏，但是遇到好行情就会大赚

- 行业策略比宽基指数收益要高很多。因为相关性不大，如果遇到好的连续大涨会收益很高

- 白云飞并不是一个神话，还是有概率获胜的成分。要多测才能发现新的机会

- 均线参数不能太大，太大了会造成大幅回撤，太小了又会造成大幅波动。

- 每种Index都有适合的参数。

- 后续工作：
  - 大量的优化如何提高速度，而不是在等待
  - 完善策略输入,比如用json格式，不是写在class中，而是从json文件读取
  - 分钟线的回测
  - 新策略如何有效利用现有代码，如果仁的最小市值、高成长策略
  - 目前可以实现的是比较简单的单个股票，如果是多个股票同时持仓，如何实现！！！！
  - 多个持仓的实现
  - 分钟线高频策略
  - 大批量数据库，sqlite/bcolz/

# 开发环境与主要库版本 (21.10.27)
- Python 3.7.7 
- win10 64位 21H1
- 

# 正式使用步骤说明
- 运行CommonModules\DataMaintain.pu，用于维护(增加）行情数据
- 运行ts00571.py
- 4个模式
  - 查询当前状态
  - 回测模式（用日线数据）
  - 实测模式（用到10分钟线）
  - 优化模式

# 参考
- test00621 getindexprice.ipynb
- https://realpython.com/python-interface/ Python Base Class、正式接口：abc.ABCMeta、Virtual Subclass
- https://www.datacamp.com/community/tutorials/inner-classes-python 嵌套类的使用
- test00253 getstockprice
- test00621 getindexprice_Tushare
- test00622 getindexprice_JQData
- https://realpython.com/python-data-classes/ 数据类讲解
- https://realpython.com/inheritance-composition-python/ 关于类的继承和组合
- https://stackoverflow.com/questions/26716616/convert-a-pandas-dataframe-to-a-dictionary 将DataFrame转为Dictionary的不同参数设置
- ffn、from empyrical import max_drawdown 金融评估包
- 

# 步骤
* 多个策略可以动态添加
** 低频C2策略
** 宽基策略
** 高频策略
** 行业策略

* 每天自动执行

* 主要就是白云飞的方法，比较X日涨幅、Y日的均线差

# 流程结构
* 多个策略
    Strategy_0101（高频）
    Strategy_0201（低频、A股几大指数）
    Strategy_0301（低频、全球几大指数）
    Strategy_0401（低频，A股行业）
    
* 获取每日数据

* 步骤：
    循环执行
        到某个时间点时，获取指数日线数据
        比较X日涨幅、Y日均线数据，N个标的进行比较
        发出当前应持有的标的
        根据现有持仓，比较是买入还是卖出

* 先实现0201策略
  
* 先在一创聚宽研究策略中实现


# 难点
## 微信发送信息
itchat，wxpy必须调用weixin网页版，目前已不能使用;
用WechatPCAPI;


# 策略分类
1. 010/020/...   ETF 轮动     策略 中国宽基策略 环球宽基策略 高频策略 行业动量策略
2. 110/120/...   最小市值类
3. 210/220/...   


# 问题及解决

1. 获取几个指数和ETF标的：

  * 000016.SH 上证50 000300.SH 沪深300 399905.SZ 中证500 399673.SZ 创业板50
  * 513030.SH 德国30 510300.SH 沪深300 513100.SH 纳指ETF 513520.SH 日经ETF 518880.SH 黄金ETF
  * 162411.SZ 华宝油气 515700.SH 新能源车 512660.SH 中证军工 512880.SH 证券ETF 512980.SH 中证传媒 512690.SH 中证酒 515070.SH CS人工智能 515000.SH 科技龙头 512480.SH 半导体

    参数 . 涨幅参数(日) VariationDays . 均线参数(日) AverageDays . VD日前日期
    . AD日前日期
    . 今日
2. 输出 当前策略的最大值对应标的 写入读取txt数据，当前策略对应的标的和买入日期
   
    数据结构 字典，关键字：指数名称，后面跟涨幅、均值差


# 策略

## 动量轮动策略
根据N日涨幅、M日均线以上、R日内不要动的算法

## 中小板最小市值策略
中小板市值最小股票

## 海龟策略



# 类及作用、相互关系

## 一览表
* Account   买卖账户及其子类，包含了Transact动作，如下单、做记录 （似乎应改为Transact类）
* BackTest  回测，主体类，属性包括Account、Strategy、Performance对象
* DataInterface   获取历史和实时行情数据接口。子类，JQDataInterface，JoinQuant数据接口，将来有其它数据用于替换
* Strategy   策略类及其子类
* RealTimeTrading   实时跟踪、下单，主体类，属性包括Account、Strategy、Performance对象
* LocalDBMaintain   本地数据维护
* Performance   回测结果计算比较
* Optimizer   回测优化，找出最佳参数
* Portofolio  多个策略的回报
* Util 工具类
* Viewer 类，将数据图像化显示
* Trading    运行
* AdpBackTest 自适应参数回测


## 逻辑流程
- 以Trading为主体，开启一次交易、初始化
- 设定Strategy策略，包括名称和起始结束日期时间
- 设定Account账户信息，包括本金、仓位、日志位置
- 设定Performance信息，包括Benchmark
- 循环根据每个bar运行策略，得到信号
- 进行交易，发送信号给微信，相当于模拟实际交易
- 计算当前操作，写入账户仓位、日志。
- 计算Performance，每个日期都有一个记录，每天的涨跌情况
- 如果是回测，最后计算总盈亏、最大回测，以及Benchmark的对比
- 如果是优化，对上面的进行多次回测，看同一个策略的不同参数


## Account 类  买卖账户及其子类，（包含了Transact动作，如下单、做记录，将Transact拿出来，主框架应该是Trading）
  - Capital  本金
  - P&L     当前盈亏
  - Logger   交易日志文件的读取、写入
  - Position  当前持仓及其读写（应该允许包括多个标的）
  - 

  CreateLoggerFile()
  ReadPosition()
  Transact()
    PlaceOrder()
    WritePosition()
    WriteLogger()
  SetPositionFileName()
  SetLoggerFileName()
  WriteLogger()

- [重构]：按实际生活理解，Account的意义和内容其实就是当前持仓、当前回报率，是一个数据类。
Transact应该独立用一个类来实现，它包含了下单、写日志、写持仓操作，它是一个动作类。


### Account_BackTest 回测类
  __CleanAllLoggerFiles()


### Account_RealTime 回测类



## Benchmark 类 

dataclass
不要放到Performance中
- Property:
    ID
    ProfitPct 参考指数收益
    MaxDrawdown 最大回测率
    Sharp Ratio...

- Function: 
    SetBenchmark(Index)
    GetPerformance(Index,startdate,enddate)
		ProfitPct=EndDayPrice/StartDayPrice-1

- 最大回撤算法
  区间最大值
  用scipy实现

- 有一个DailyLogger，创建 


## DataFeeder
公共数据接口，可以切换数据来源，如JQData/LocalDB，但是对程序的接口一样，将来更换数据不用改代码

- [ ] 如何通过继承、多态指定数据来源？
方法：父类申明方法，在子类中实现；调用前，先创建对象

- [ ] 类的静态方法是否可以多态？

父类，
DataFeeder 
  def GetPriceDFofTheTime(index,thedatetime,IncludeNow=True):
  def GetDayPriceBar(index,days,enddate,IncludeNow=False):
  def GetTheDateTimePrice(index,thedate,thetime):
  def GetSecurityName(Index):
  def GetTradingDays(startdate,enddate):

子类  
JQDataFeeder
TSDataFeeder
LocalDataFeeder

* 可以用类似BackTester的get(provider='')来实现

## DataMaintain
- 数据维护类
  数据表更新
  指数表
  日线数据更新
  分钟线数据

-指数日线从2006-1-1开始
分钟线从2019-1-1开始

- Property:
  DayBarPathName    C:\Users\Aaron\Documents\MyMobileBooks_800_Reading\MyTSSnippets\DataRepository\db00071\Day
  MinuteBarPathName C:\Users\Aaron\Documents\MyMobileBooks_800_Reading\MyTSSnippets\DataRepository\db00071\Minute
  IndexListCSVPathName (用NamedTuple表示？)  C:\Users\Aaron\Documents\MyMobileBooks_800_Reading\MyTSSnippets\DataRepository\db00071\codelist.csv
  IndexList

- Function:
def RunMaintain():
  获取今日日期

  循环所有的CodeList和文件，进行更新
  for each Index
    ExportDayBar2CSV()
    ExportMinuteBar2CSV()

FetchDayBar2CSV(IndexID,startdate,enddate)
  格式:date, minute(15:00), open, high, low, close

_GetExistingEndDate()  #查看现有日期中的日期范围，enddate是哪一天
  对不在日期范围内的进行添加

FetchMinuteBar2CSV(IndexID,startdate,enddate)
  格式:date, minute, open, high, low, close

  _GetExistingDatesScope()  #查看现有日期时间范围
  对不在日期范围内的进行添加


## Optimizer 类
- 	目的
将不同回测的Performance进行比较，找出最佳的回测对应的Performance参数。这里的主体是多个回测对象Trading_BackTest。
所以，一次回测应该对应一个对象。对回测进行优化，获取一个最佳的参数，比如N日涨幅、M日均线值

- 包含的优化对象

  - 	时间：9:40~14:50，哪个时间段下单是最好的
  - 	参数：比如涨幅日期、均线日期
  - 	ETF List：哪个ETF是最优的

- 参数列表：

  - 	动态函数
  - Parameter list组合
    如

-	Optimizer结果：
  参数A/B 对应的收益、最大回撤

  应该是从不同的logger文件读取

- 输入：
  
- 策略、参数、起始日期、结束日期
  
- 过程：
  - 参数组合的集合 (1,1)/(1,2)/.....(15,15)
  - 获取某个参数的Performance结果。最后对所有集合进行排序。获取一段时间的最佳参数

- 输出：
  - 最佳参数组合，以及结果
  - 一个csv文件，
    -parameter1/parameter2/.../Performance.收益/Performance.最大回测


- 是一个上级类，包括多个Trading_BackTest，对同一个策略不同的参数进行比较。
或者不同策略不同参数的比较

- 属性
	* 参数集合
	* 	日期
	* 时间
	* BackTest 列表
    
  * 优化结果列表
     * 
- 方法
  Run()

- Task
  - 将VRDate/AVDate做一个数据组合，如2~20/2~20
  - 

- 中间的Logger文件不用实体保存，而用一个df保存？没有必要，可以单独设置一个文件夹
​	
## Performance 类
-作用：

- Property:
  startdate   起始时间
  enddate     结束时间
  Profit      收益额
  ProfitPct   收益率
  MaxDrawdown 最大回测率
  Sharp Ratio 夏普比例
  MaxPrice    区间最大值
  MinPrice    区间最小值
  TradeCount  交易次数
  WinCount    盈利次数
  LossCount   亏损次数
  WinRate     获胜次数

  LoggerFilePathName
  Logger  日志文件

- Function:
  - 列出每年的收益回报、最大回撤 
    

## Performance_Simple 类
* 仅仅计算比例，不考虑现金、股份等因素

- Property: 

- Function:
  -根据动态交易计算，用于实时交易。每次买卖后显示前一笔盈亏比例和当前市值，从1开始。
  GetPerformance_Sync()
    (放在每笔交易后)
    if Buy
      BuyPositionPrice=ReadPostionPrice()

    else Sell
      Capital=SellPositionPrice/BuyPositionPrice
  

  -根据日志文件盘后计算，用于回测。不过回测也可以用动态同步计算
	GetPerformance_Async(index)
    _ReadLoggerFile()
    for each Transaction in TransList:
      if Buy
        BuyPositionPrice=ReadPostionPrice()
      else Sell
        Capital=SellPositionPrice/BuyPositionPrice
		
	-创建DailyLog，便于显示盈利日线，只要看交易日即可



## Portofolio 类
持股池
比如1/3用策略1，1/3用策略2、1/3用策略3，


## Transact 类 
替换之前的Account类
模拟单次交易过程，下订单（发送信号）、读写Position文件、读写Logger文件
  PlaceOrder()

  

## Trading 类，框架类
包含了一次活动，比如回测、实时交易
其中有策略、账户、盈亏表现
  - theStrategy 即时的策略对象
  - theAccount  即时的账户（也可以说是Transaction)对象
    (Account账户、Transaction账户应该分开？)
  - theTranaction 即时单次交易过程
  - thePerformance  即时的回报率对象

  .Signal/.SignalIndex/.SignalPrice

### Trading_Interactive 类
  for each strategy 
    GetTransactionSignal


#回测
### Trading_BackTest 类
  只针对一个BackTest对象，不要包含多个。

  Run()
	输入参数
    RunStrategy()
    RunTransaction() #对每个策略、每一天进行回测
    RunPerformance() #对测试结果进行计算，打印回报率、回撤率。同时计算Benchmark的回报率、回撤率

#实时监控，有点像模拟交易
### Trading_RealTime
  Run()
    RunStrategy()
    RunTransaction()
    RunPerformance()

#对回测进行多次测试，找最优值
### Trading_Optimize
  Run()


## Strategy
  输入：日期、时间点
  输出：每个策略对应的信号

  用于制定策略，获取买卖点信号

  #获取单个指数的涨幅、均线差值比
  GetIndexVR_AV(self,index, thedate,thetime)

  #获取最优Index,返回信号
  GetTransactionSignal(self,thedate, thetime) 


## Viewer
* 目的：
  * 显示回测盈利图
  * 显示价格线
* 属性
  * 
* 方法

# Learning Points

* 将日期字符串转为DateTimeIndex
dfnew['Date'] = pd.to_datetime(df['Date'])
dfnew.set_index('Date',inplace=True)

* 几个参数的组合
GetCombination = lambda x, code=',': reduce(lambda x, y: [str(i)+code+str(j) for i in x for j in y], x)
GetCombination(lists1,',')

* Tips: 为避免程序运行完毕还没来得及看结果程序窗口就已经关闭了，我们可以在代码最后一行加上：
raw_input("Press Enter key to exit.")

* 修改dataframe的一列输出格式
  df['col']=df['col'].apply(func)

* 读取csv保存为DataFrame
with open(self.LoggerPathName) as file_obj:
            
    reader = csv.reader(file_obj)

    for row in reader:
        tmp_lst.append(row)

self.dfLogger= pd.DataFrame(tmp_lst[2:], columns=tmp_lst[1]) 

* 将yyyy-mm-dd改为yyyymmdd startdate =datetime.datetime.strptime(startdate, '%Y-%m-%d').strftime('%Y%m%d')
或者 datetime.today().strftime('%Y-%m-%d')

* dataframe日期排序 df_AV.sort_values(by='trade_date', inplace=True, ascending=True)

* 如何看待工作日和实际需要的日期

* 计算均线，rolling, mean, shift的用处 df_AV['ma'] = df_AV['close'].rolling(g_AVDays).mean().shift(g_AVDays-df_AV_rows)

* 昨天、前天日期的获取 datetime.datetime.today() - datetime.timedelta(days = 2)

* 小数变为百分数 a = 0.3214323 bb = "%.2f%%" % (a * 100) print bb

* 百分数变为小数 float(dicAV[d_order[0]].strip('%'))

* 每个指数对应涨幅、日K线的数据结构 不能用字典，因为只是1对1，应该用dataframe结构,或者用多个dict

* 字符串转为日期 datetime.datetime.strptime(enddate,'%Y%m%d')

* 日期转为字符串 string1.strftime('%Y%m%d')

* 字典的内部排序 d_order=sorted(dicVR,key=lambda x:x[1],reverse=True)

* 获取过去n日的数 据，不含节假日 用JQData，pip install jqdatasdk 或者用tushare，但是要用交易日历排除

* 动态生成类 
  dynclass=globals()['c1']
  instance = dynclass()

* 日期连续生成
a = datetime.datetime.strptime('2019-04-29' ,'%Y-%m-%d')
b = datetime.datetime.strptime('2019-05-03' ,'%Y-%m-%d')
for i in range(a.toordinal(), b.toordinal()):
    print(datetime.date.fromordinal(i))

* 数据类 @dataclass
好处：定义时简单，不用__init__写一堆

* 一个类包含了另一个类的列表，这个可以用在如优化Optimizer计算，得到多个回测Performance对象，然后进行逐一比较。或者多个Strategy对象，进行比较优劣
@dataclass
class PlayingCard:
    rank: str
    suit: str

@dataclass
class Deck:
    cards: List[PlayingCard]

* 如何调用私有方法()
  私有函数前面是_ _，再加一个_Classname
dog._Dog__format1()

* MarkDown语法
  

**粗体**
*斜体*
~~划线~~
___

* DataFrame日期数据中，将index设为date，可以直接调用df['2019']这样直接选择2019年的数据
df['date'] = pd.to_datetime(df['date'])
df.set_index('date', inplace=True)
可以直接选择某个日期区间的数据，如
df.loc['2020-07-01':enddate]
或
df.loc[:enddate].tail(x) 选择某结束日期前几天
或 
df[df.some_date.between(start_date, end_date)]
或
df['date'] = pd.date_range('2017-1-1', periods=30, freq='D')

* df.loc[thedatetime].to_frame() 单个label返回是series，需要用to_frame()转换为DataFrame
但是还不够，这里返回的需要用.T，df.loc[thedatetime].to_frame().T，否则是一个未转换前的形式

* DataFrame转为字典dict，需要转换 ，这样才能将第一列作为index，第二列作为对应值
df.set_index('ID').T.to_dict('list')
或者
pandas DataFrame数据转为list
首先使用np.array()函数把DataFrame转化为np.ndarray()，再利用tolist()函数把np.ndarray()转为list，示例代码如下：
# -*- coding:utf-8-*-
import numpy as np
import pandas as pd

train_data = np.array(data_x)
train_x_list=train_data.tolist()#list
print(train_x_list)
print(type(train_x_list))


* 回测时间慢，虽然换到本地数据，但是还是很慢。经过查找时间，发现主要问题主要出在DataFeeder的df=self._GetDataFrame，就是每次都要取一次时间数据，都要从csv读出所有的数据，然后再找。效率很低。

* import 头文件能否实现？这样避免每个module都要import相同的东西


* 删除不含内容的数据

nan_value = float("NaN")
df.replace("", nan_value, inplace=True)
df.dropna(subset = ["open"], inplace=True)


* dataframe可以匹配字符串
df[df['model'].str.match('Mac')]

*  dataframe的mask实现
First, lets ensure the 'birth_date' column is in date format
df['birth_date'] = pd.to_datetime(df['birth_date'])
next, set the desired start date and end date to filter df with
-- these can be in datetime (numpy and pandas), timestamp, or string format
start_date = '03-01-1996'
end_date = '06-01-1997'
mask = (df['birth_date'] > start_date) & (df['birth_date'] <= end_date)
assign mask to df to return the rows with birth_date between our specified start/end dates
df = df.loc[mask]
df

* 修改数据类型从DateTime到String
  TradingDaysList=map(str,TradingDaysList)

* 将DataFrame中的一行进行操作
self.dfDailyLoggerRegular['close']=self.dfDailyLoggerRegular.apply(lambda x: x/PreviousDayClosePrice,axis=1)    