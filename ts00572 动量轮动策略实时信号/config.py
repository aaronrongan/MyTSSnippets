


global g_SelectedMode

# 调试模式，不要发送手机短信、可以输出打印调试信息
global g_debugmode
# g_debugmode=True

global g_PhoneMessageSwitch
g_PhoneMessageSwitch=False

# WeChat开关
global g_WechatSwitchOn
g_WechatSwitchOn=False

# 静态模式，不要发送中间输出信息
global g_silentmode
g_silentmode=True

# 策略运行间隙时间
global g_seconds_strategyinterval,g_seconds_runinterval
g_seconds_strategyinterval=1
g_seconds_runinterval=30

# 初始化数据接口
# 不同数据来源，使用同一个接口
global g_DataFeeder,g_JQDataFeeder
g_DataFeeder=None
g_JQDataFeeder=None

# 初始化微信接口
global g_wechat
g_wechat=''

global g_TradingDaysPathName
g_TradingDaysPathName="C:/Users/aaron/Documents/MyMobileBooks_800_Reading/MyTSSnippets/DataRepository/db00131/tradingdays.csv"


g_DayBarPath = 'C:/Users/Aaron/Documents/MyMobileBooks_800_Reading/MyTSSnippets/DataRepository/db00071/Day'
g_MinuteBarPath ='C:/Users/Aaron/Documents/MyMobileBooks_800_Reading/MyTSSnippets/DataRepository/db00071/Minute'
g_Minute10BarPath ='C:/Users/Aaron/Documents/MyMobileBooks_800_Reading/MyTSSnippets/DataRepository/db00071/Minute10'
g_IndexListCSVPathName='C:/Users/Aaron/Documents/MyMobileBooks_800_Reading/MyTSSnippets/DataRepository/db00071/IndexList.csv'

g_StockCodeListPathName='C:/Users/Aaron/Documents/MyMobileBooks_800_Reading/MyTSSnippets/DataRepository/db00011/stockcodelist_jq.csv'

# 持仓保存文件路径（不含文件名）
g_Data_BackTest='C:/Users/Aaron/Documents/MyMobileBooks_800_Reading/MyTSSnippets/ts00571 动量轮动策略实时信号/Data_BackTest/'

g_Data_RealTime='C:/Users/Aaron/Documents/MyMobileBooks_800_Reading/MyTSSnippets/ts00571 动量轮动策略实时信号/Data_RealTime/'

g_Data_Optimizer='C:/Users/Aaron/Documents/MyMobileBooks_800_Reading/MyTSSnippets/ts00571 动量轮动策略实时信号/Data_Optimizer/'

g_Path_CommonModules='C:\\Users\\Aaron\\Documents\\MyMobileBooks_800_Reading\\MyTSSnippets\\CommonModules'

g_DefaultStartDate='2021-07-01'

g_DefaultEndDate='2021-08-31'
