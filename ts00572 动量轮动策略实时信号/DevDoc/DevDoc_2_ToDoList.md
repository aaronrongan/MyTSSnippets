# To Do List

- [x]  获取交易日，倒数N天要能避开周末、节假日(或者找一个现成的库和函数）
- [x]  用class 实现，一个策略对应一个class 
*   输出结果用一个DataFrame来表示，看上去简洁
- [x]  保存一个文件，上面用买入仓位标记
*   输入：
    *       每个策略的VR、AV值默认或者重新输入      参考ts00061 财报下载
    *       可以单次查询、也可以无限循环（每隔3分钟）参考ts00521 白云飞信息自动监控
*   输出：当时产生信号对应的代码及名称  
    *   输出各个指数的数据，规划化、看起来清楚
    *   一次查询、循环执行
- [x]   下载所有ETF和相关指数5年数据，便于离线回测

- [x]   回测类实现

- [x]   持仓文件，除了写入index号，还要有当时的价格，便于计算Performance

- [x]   Realtime模式下，实时发送微信信息，比如超过某个点，比如今日的军工ETF买入

- [x]   RT和BT模式下，Logger文件的创建

- [x]   发送WeChat消息，特别是实时有信号产生时发出

- [x]   交互模式用Q再返回，否则一直循环查询

- [ ]   网格策略的编写。如何和现有策略共用同一个父策略

- [ ]   ETF轮动策略中，P日后才能动，这个参数如何使用

- [x]   对回测进行优化，获取一个最佳的参数，比如N日涨幅、M日均线值
        Optimizer类
	
- [ ]    将010/020/030这3个策略合并一个类，没有必要针对不同的股票池来做多个类

- [ ]    编写中小板最小市值策略

- [x]    按5分钟线级别进行回测

- [ ]    BackTest中的.Signal/.Selectedindex/.Price应该放到strategy中

- [x]   将Realtime/BackTest/Interactive整合到一个大类
        Trading

- [x]    将调试输出信息用g_silentmode表示

- [ ]    输出信号用一个整齐的格式：Index  IndexName N日涨幅  M日均线  当前价格
        最好用DataFrame，df_output来实现
	
- [ ]    将策略类做成更广含义，不仅仅限于动量轮动策略，还有网格、海龟等策略
        Strategy010/020/030能否合并到一个类中，主要区别其实就是ETFList，没有必要做成独立的类
        PositionFileSavePath、LoggerFileSavePath能否不要放到Strategy中

用txt文件存放策略参数，放入到Data_Strategy文件夹
	
- [x]    ReFc:重构 GetBestIndex() 统一为GetTransactionSignal()

- [ ]    加入R天参数后才买卖

- [ ]    JQData GetDayPrice，参数IncludeNow=TRUE似乎不起作用

- [ ]    引用为什么每次要用sys.path.append?

- [x]    回测绩效的实现

- [ ]    编写一个公共数据接口类，可以切换JQData、本地数据。比如在Init时，制定数据来源，但是程序中不用管数据从哪来的
        参考BackTester如何实现(provider='')

- [ ]    遇到大跌没有事先计划，看着下跌，幻想马上上升。要提供一个功能，能够提前预警，距离还有多少点。否则到了点舍不得下手。

- [x]    将GetVRDays、GetAVDays统一一个函数来表示

- [x]    实现Optimizer，进行多次回测

- [x]    计算程序运行时间，减少等待。比如做一个本地tradingdays、indexlist

- [x]    DataMaintain加入本地tradingdays的维护

- [ ]    DataMaintain的启动：比较一个文件上次修改时间，如果现在是上次修改日期第二天的下午3点后就进行维护

- [x]    回测的最后一行，应该显示Enddate的持仓价格

- [x]    交互模式下，将silentmode作为可选项，简洁输出

- [x]    实现Optimizer，一个是找到合适的参数，一个是卖出时间；

- [ ]    实现高频监控，能否找到每天何时卖出才是最合适的

- [ ]    将动量Strategy统一为一个，不要分成多个子类

- [x]    在回测日志文件中，加入该回测的参数、尾部加上回测的盈利

- [ ]    在回测的弹出信号上，加上各指数ETF对应的涨幅和即将突破的数值，便于知道哪个指数即将产生信号

- [ ]    输出信号/发送WeChat消息有问题，要什么时候需要输出信息、什么时候需要收到WeChat指令。Strategy、Transaction到底谁来发送信号要分清楚

- [x]    计算Performance每日累计收益，并能绘制出

- [ ]    在区间图上绘制出买卖点

- [x]    在StrategyLogger中加入本次盈亏、累计盈亏

- [ ]    实时模式，是否需要在如14:30买点才发送提醒信号？

- [ ]    搜集2018/2019年的本地分钟线数据，这样回测才准。为了降低体积，可以只搜集5分钟或者10分钟线数据

- [ ]	回测模式，参数输入只要做一次，后面几个策略不用再输入参数

- [x]	建立5/10分钟线回测数据，从2015年开始。将Minute数据都放入

- [ ]	输出显示信息时，能根据当前运行模式来决定打印哪些内容

- [ ]	用一种掩码的方式来判断多个条件是否该打印需要的内容，或者用自定义Print的方式

- [ ]	time和datetime.time有什么区别？为什么经常会报错：time.XXX没有这个属性

- [ ]  	ETF List读取增加识别#功能，如果有，相当于注释，不使用

- [ ]  	回测Performance实现分年度、分月度的performance输出，便于统计
        用FFN就可以轻松实现

- [x]  	将大的类独立放置为一个文件，比如Strategy、Performance

- [x]  	Logger第几行要加入运行参数说明，AVDays:13,VRdays:5

- [x] 	StrategyPosition加入参数说明

- [ ]  	查为什么信号(20-07-31)明明是创业板板强势，但是发出的却是沪深300的信号
  
- [x]  查询模式下，如果不是交易时间，应该取最近的一天的收盘数据
  
- [ ]  涨幅大于0、比均值大于0，这里的0是不是应该设置一个阈值，比如0.01%，-0.02%不应该被考虑是一个有效的信号

- [ ]   GetIndexVR_AV，用聚宽一样的算法（前一日价格而不是当前价格），是否能够和聚宽结果基本一致

- [ ]   FFN包是如何将一个DataFrame转换为其使用的对象的？

- [ ]   PerformanceList开头行加入参数、运行日期

- [ ]   Optimizer速度太慢，能否不用文件保存，而用内存方式读取？
  
- [ ]   设置路径的统一根目录字符串全局变量，这样就能实现修改文件路径

# Logger


* 211027
- []    重新开始使用该系统，JQData数据收费，改为TuShare接口，增加TSDataFeeder

* 200809
- [x]   重新编写Performance的DailyLogger求解，前一版太乱，想到哪写到哪，到后面越改越难。
经验：在纸上写出所有的可能，然后写出流程图，这样一气呵成。第一版花了5~6个小时还是一头雾水，第二版花了1个半小时全部写好
- [x]   完成maxdown计算。利用ffn包。
- [x]   解决一些bug。如Benchmark的P&L计算，因为apply错误，应该用x['close']/Previous,而不是x/Previous...
self.dfDailyLoggerRegular['close']=self.dfDailyLoggerRegular.apply(lambda x: x['close']/PreviousDayClosePrice,axis=1)    
       

* 200808
- [x]   完成Performance的日志求解，为策略表现做好准备

* 200807
- [ ]   增加codelist获取。可以进行所有的code的高成长和最低市值的查询

* 200807
- [x]	完成DailyLogger算法

* 200804
- [x]	初步完成Optimizer，对AVDays/VRDays进行组合回测

* 200803
- [ ]	找到解决bug，CurrentPrice改为SelectedPrice

* 200802
- [x]	将类做成单个文件，便于管理
- [x]   完善Strategy，打印出清楚的格式

* 200801

- [x]	Logger文件完善CurPL,CumPL
- [x]	GetTradingDays 为什么要2次
- [ ]	做出每笔交易后的格式清单，每个ETF有多少涨幅、和均线差值

* 200730
- [x]	完善10分钟线数据采集
- [x]	解决bug: 查询模式、IsTradingDays()、 
- [x]	实现10分钟线的数据转移，可以实现2015年的回测

* 200729
- [x]	计算最大回撤。
- [x]	程序bug改进。
- [x] 	将查询模式输出内容用DF来表示，显示各ETF当前的涨幅排名，像聚宽那样
- [x]	监控模式，能运行时指定微信是否启动

* 200728
- [x]   成功提高回测速度，不能用网上数据、不能在运行时读取csv，改用LocalDataFeederMemory，在创建Data对象时一次性调入所有的价格数据  

* 200727
- [x]	实现回测。其它程序bug修改。
- [x]	完成Performance其它信息的统计

* 200726
- [x]	回测计算，求出单次计算结果并显示
- [x]	DataMaintain的更新，对于其它数据也要进行更新 

* 200725
- [x]   完成本地日线和分钟数据抓取，DataMaintain维护，实现每天或某天的动态数据更新。不足在于没有检查机制、只能加后面的数据不能加前面的数据
- [x]   完成LocalDataFeeder，关键是DataFrame的运用，找出符合某个条件的日期对应的日线、分钟线数据 参考 https://zhuanlan.zhihu.com/p/27094705 

* 200724
- [x]  	 没有必要将所有的函数都用本地数据接口来实现，有一些做不到。只有日线数据可以

- 200723
- [x]	引用然后调用WeChatPCAPI成功。原来要将.ipy、.exe、(lib)文件夹都包含在内。
另外，将模块作为一个公共模块的方法：
import sys 
 sys.path.append('C:\\Users\\Aaron\\Documents\\MyMobileBooks_800_Reading\\MyTSSnippets\\WeChatAPIWrapper')
        from WeChatAPIWrapper import WeChatAPIWrapper

- [x]	完成实时监控时交易信号报警，成功将回测信息发送到微信界面。实现实时提醒信号。


* 200722
- [ ]	完成回测计算

* 200718
- [x]	周末两天完成ts00571.py，主要类的编写，主要功能实现

* 200715 
- [x]	test00622 getindexprice-JQData Jupyter代码，原型测试
