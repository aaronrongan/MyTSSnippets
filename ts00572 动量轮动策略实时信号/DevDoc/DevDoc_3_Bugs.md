
- [x]    ===515000.XSHG=== 后面加入对应名称

- [x]    ===所有均线。。。。=== 加入策略名称、参数

- [ ]    计算涨幅时，应该从前一日开始，而不是算到今日

- [x]    排名出错，
    原因：1.%,2%这些格式因为要显示为小数点，导致形成字符串进行比较，而不是浮点数

- [x]    排名错误d_order=sorted(dicVR,key=lambda x:x[1],reverse=True)    
    应该用dicVR.items()对值排序
    d_order=sorted(dicVR.items(),key=lambda x:x[1],reverse=True)    

- [ ]    计算GetBestIndex时，如果是回测，在计算日期时，比如昨天早上10点的回测，那么应该用前日的close价格计算，而不应该用昨日的收盘线
JQData的函数get_bars(include_now=False)

- [x]    BackTest类中，PlaceOrder时，如果前一天买的，但今天的信号是买入其它股票，那么应该先卖出之前的，才能买入今天信号的

- [x]    return 'BUY', str(d_order[0][0]),round(d_order[0][1],2) #包括Index及价格 
  - 这里不是返回价格，而是返回的涨幅
  
- [ ]  是否应该将Account替换Transact

- [ ]  BackTest每一步都要输入日期
        解决：在RunStrategy前放一个InitStrategy

- [x]  应该将一次回测作为一个对象。而不是现在的Trading_BackTest包含了多个回测
  
- [ ]  回测速度太慢，是不是因为从网络获取数据导致？比如get_security_name()。要用本地数据代替、
        可以在MainInit()中读取一个global dict或tuple，这样就不用每次都要JQData获取名称

- [ ]  本地数据取超过当前日期时间的价格时，要有判断，如果超过的话，返回最后一条数据

- [x]   Benchmark的收益率计算，不应该取startdate/enddate，应该是取startdate-1的收盘价、enddate当天的收盘价

- [x]   Performance的收益率计算，如果最后一天买入，最后还要计算enddate当天持仓的收盘价，再进行一次计算，而不是算到那天的买入价  

- [x]    回测文件的Position文件要清空，不能用上次的

- [x]   清理某些文件时，listdir不能找到指定字符串的文件夹
要用glob

- [ ]   无法读取文件exception:[Errno 13] Permission denied: 'C:\\Users\\Aaron\\Documents\\MyMobileBooks_800_Reading\\MyTSSnippets\\ts00571 动量轮动策略实时信号/Data_BackTest/StrategyPosition_020.csv'
是否要过10秒再次读取？
while(1)

- [x]    实时模式，不是交易日、周末、中午时间、9点半前、3点后应该不要采集数据
  
- [x]    要想回测好，必须保存好当年的分钟线数据，除非用收盘数据   

- [x]    回测默认结束日期，最好是按库中的最后一天日期，否则测试无效。目前应该是白天按前一天，晚上按当日数据

- [ ]    读取Logger文件时，因为坚果云的同步，导致经常会占用资源导致读取错误

- [ ]   单次查询模式，当时间超过15:00时，报错"C:\Users\Aaron\Documents\MyMobileBooks_800_Reading\MyTSSnippets\CommonModules\DataFeeder.py", line 380, in GetPriceDFofTheTime
    return df.loc[thedatetime].to_frame().T
	
- [ ] 	python type object 'datetime.time' has no attribute 'localtime' 
方法： import time as t

- [x] 	日线等数据的维护对于空数据，不要放入数据库，减少体积
方法： 获取数据时，将空数据作为NaN，然后dropna

- [ ] 	取日线数据，如果要求的日期并不是trading days，要找到适合的最近的日期

- [x] 	为什么IsTradingDays出错，df['2020-07-30']返回empty？因为只有1列date，将其设置为index后，内部就认为是空的

- [ ]	2015年的回测，行业数据会显示index out of bounds

- [ ]	全局变量的使用要谨慎，当将模块分到不同文件时，就出现了问题。
  
- [ ]	回测时，获得价格数据错误，self.CurrentTimePrice是最后一次ETF的价格，不是选中Index的价格
  print(thedate, thetime, ': BUY', self.dfOutput.loc[0,'Index'],str(self.dfOutput.loc[0,'IndexName']),self.CurrentTimePrice )

- [x]	回测时，取N日均线涨幅，不能取当日的，比如14:30发出信号，不能用当日的15:00来回测。聚宽是用前一日的，但是实际计算应该取当日14:30的作为最新的计算
  代码是对的：changepercent_VR=(self.CurrentTimePrice-df_VR['close'][0])/df_VR['close'][0]

- [x] 优化模式，第一个参数结果是对的，第二个参数结果是错的，因为Pos文件在第二次运行前没有清空

