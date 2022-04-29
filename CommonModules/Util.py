
import sys
sys.path.append('C:\\Users\\Aaron\\Documents\\MyMobileBooks_800_Reading\\MyTSSnippets\\CommonModules')
sys.path.append('C:/Users/aaron/Documents/MyMobileBooks_800_Reading/MyTSSnippets/ts00571 动量轮动策略实时信号')
import config

from abc import ABC
import datetime
import time as t
import os
import pandas as pd

# global g_TradingDaysPathName


# 工具类，一些常用的静态方法
class Util():

    def __init__(self):
        super().__init__()

        
    # 当日开盘前且为交易日
    @staticmethod
    def IsBeforeBell():
        # 如果是当日收盘前，按前一天的数据，如果是当日收盘后，按当日数据回测（不过还得做成看数据库最后一天日期）
        curenttime=datetime.datetime.now()

        d_time=datetime.datetime.strptime(str(datetime.datetime.now().date())+'9:30', '%Y-%m-%d%H:%M')

        defaultenddate=Util.GetTodayDateString()

        if curenttime >=  d_time:
            return False
        elif curenttime <  d_time:
            return True

    # 下午收盘后
    @staticmethod
    def IsAfterBell():
        # 如果是当日收盘前，按前一天的数据，如果是当日收盘后，按当日数据回测（不过还得做成看数据库最后一天日期）
        curenttime=datetime.datetime.now()

        d_time=datetime.datetime.strptime(str(datetime.datetime.now().date())+'15:30', '%Y-%m-%d%H:%M')

        defaultenddate=Util.GetTodayDateString()

        if curenttime <=  d_time:
            return False
        elif curenttime >  d_time:
            return True

    @staticmethod
    def Float2Percent(floatnumber):
        return "%.2f%%" % (floatnumber * 100)
    
    @staticmethod
    def Percent2Float(PercentNumberString):
        # PercentNumber.replace('1','')
        PercentNumberString=PercentNumberString.split('%')[0]
        # print(PercentNumber)
        
        
        return float(PercentNumberString)/100

    @staticmethod
    # 将日期格式转为YYYY-MM-DD
    def DatetoString(theDate):
        
        return theDate.strftime('%Y-%m-%d')

    @staticmethod
    # 将YYYY-MM-DD转为日期格式
    def StringtoDate(String):
        theDate=datetime.datetime.strptime(String,'%Y-%m-%d')   
        return theDate

    @staticmethod
    # 输入旧日期字符串，返回新日期字符串
    def DateDelta(OldDateString, count=0):
        
        olddate =Util.StringtoDate(OldDateString)

        # 计算偏移量
        offset = datetime.timedelta(days=count)

        # 获取修改后的时间并格式化

        newdate = (olddate + offset).strftime('%Y-%m-%d')

        return newdate

    @staticmethod
    # 发送手机短信消息 
    def SendPhoneMessage(message):
        # Your Account SID from twilio.com/console
        account_sid = "AC412d0f21432ea42fe2f9068b7a26fd35"
        # Your Auth Token from twilio.com/console
        auth_token  = "7c996ef074f8ddbdf5fe200333a41c9c"
        
        client = Client(account_sid, auth_token)

        for each in range(1,2):
            message = client.messages.create(body=message + str(each), from_='+16606754209', to='+8617312656875') 
            time.sleep(1)
            #print(message.sid)
            
    @staticmethod
    # 发送邮件消息        
    def SendMail(message):
        
        mail=smtplib.SMTP('smtp.office365.com',587)
        mail.starttls()

        mail.login('aaronyinyong@hotmail.com','yinrong090114')
        message = MIMEText(message, 'plain', 'utf-8')   #发送的内容
        message['From'] = Header("持有变动信息", 'utf-8')   #发件人
        message['To'] ="todo@mail.dida365.com"   #收件人
        subject = '持有变动信息'
        message['Subject'] = Header(subject, 'utf-8')  #邮件标题
        
        mail.sendmail('aaronyinyong@hotmail.com','todo@mail.dida365.com',message.as_string())
        
        mail.close()

    # @staticmethod
    # # 发送微信消息
    # def SendWechat(message):
        
    #     pass

    @staticmethod
    def GetCustomizedDays(inputstring, defaultDays):
        theDays=str(input('输入' + inputstring  +':[' + str(defaultDays) + ']:'))
        if theDays=='':
            theDays=defaultDays
        return theDays

    @staticmethod
    def GetVRDays(defaultDays):
        VRDays=str(input('输入涨幅日期[' + str(defaultDays) + ']:'))
        if VRDays=='':
            VRDays=defaultDays
        return VRDays

    @staticmethod
    def GetAVDays(defaultDays):
        AVDays=str(input('输入均线日期['+ str(defaultDays) + ']:'))
        if AVDays=='':
            AVDays=defaultDays
        return AVDays

    @staticmethod
    # 从用户输入需要查询的日期
    def GetDate():
        theDate=str(input('输入日期['+ datetime.datetime.today().strftime('%Y-%m-%d') + ']:'))
        
        if theDate=='':
            theDate=datetime.datetime.today().strftime('%Y-%m-%d')
        return theDate

    @staticmethod
    # 从用户输入需要查询的时间
    def GetTime():
        theTime=str(input('输入时间['+ t.strftime("%H:%M:%S", t.localtime())  + ']:'))
    
        if theTime=='':
            theTime=t.strftime("%H:%M:%S", t.localtime()) 
        return theTime

    @staticmethod
    # 获取%Y-%m-%d %H:%M:%S形式的日期时间
    def GetLongDateTime():
        theDateTime=t.strftime("%Y-%m-%d %H:%M:%S", t.localtime()) 
        return theDateTime[2:]
    
    @staticmethod
    # 获取%Y-%m-%d形式的日期时间
    def GetTodayDateString():
        theDateTime=t.strftime("%Y-%m-%d", t.localtime()) 
        return theDateTime

    @staticmethod
    # 获取20-07-19_09:00:30形式的日期时间
    def GetShortDateTime():
        theDateTime=t.strftime("%Y%m%d_%H%M%S", t.localtime()) 
        return theDateTime[2:]

    @staticmethod
    # 从用户输入需要测试的策略ID号
    def GetStrategyIDList():
        theStrategyIDList=str(input('输入策略ID号-0.所有策略；010.中国宽基;020.环球宽基;030.行业ETF:[0]'))

        if theStrategyIDList=='' or theStrategyIDList=='0':
            theStrategyIDList=['010','020','030']
        else:
            theStrategyIDList=theStrategyIDList.split(';')

        return theStrategyIDList

    # 如果日期不是交易日期，获取传入日期的前一天交易日期
    @staticmethod
    def GetCloseBeforeTradingDate(theDate):
        df=pd.read_csv(config.g_TradingDaysPathName,names=['date'])
        if df[df['date']==theDate].empty==True:
            return df[df['date']<theDate].tail(1)['date'].to_list()[0]
        else:
            return theDate

    # 如果日期不是交易日期，获取传入日期的后一天交易日期
    @staticmethod
    def GetCloseAfterTradingDate(theDate):
        df=pd.read_csv(config.g_TradingDaysPathName,names=['date'])
        if df[df['date']==theDate].empty==True:
            return df[df['date']>theDate].head(1)['date'].to_list()[0]
        else:
            return theDate

    @staticmethod
    #获取某个交易日的Delta天数的交易日期
    def GetDeltaTradingDate(theDate,delta=0):
        
        df=pd.read_csv(config.g_TradingDaysPathName,names=['date'])
        # print(type(df[df['date']==theDate].index))
        # print(df['2019'].tail(10))
        # print(df['2020'].head(10))
        # print(df[df['date']==theDate])
        if df[df['date']==theDate].empty!=True:
            matchedindex=int(df[df['date']==theDate].index.tolist()[0])
        else:
            dfnew=df[df['date']>theDate].head(1)
            # matchedindex=int(dfnew[dfnew['date']==theDate].index.tolist()[0])
            # print(dfnew)
            # print(dfnew['date'].to_list()[0])
            # print(df.tail(2))
            matchedindex=int(df[df['date']==dfnew['date'].to_list()[0]].index.tolist()[0])

        DeltaIndex=matchedindex+int(delta)

        return df.loc[DeltaIndex,'date']

    @staticmethod
    #判断是否是交易日
    def IsTradingDays(datestring):
        
        df=pd.read_csv(config.g_TradingDaysPathName,names=['date'])
        # print(df.tail(2))
        # print(type(df['date']))
        # df.set_index('date', inplace=True)
        # print(df.tail(2))
        # print(datetime.datetime.strptime(datestring,'%Y-%m-%d'))

        # df=df[Util.StringtoDate(datestring)]
        # df=df[datetime.datetime.strptime('2020-07-30','%Y-%m-%d')]

        # df=df['2020-07-29']
        df=df[df['date'].str.match(datestring)]

        if df.empty!=True:
            return True
        else:
            return False

    @staticmethod
    #返回最近的一个交易日
    def GetLastTradingDay(datestring):
        
        df=pd.read_csv(config.g_TradingDaysPathName,names=['date'])
        
        
        df.set_index('date', inplace=True)
        
        df=df[datestring:datestring]
        
        if df.empty!=True:
            return True
        else:
            return False

    @staticmethod
    #判断是否是周一到周五
    def IsWorkingDays():
        week_day_dict = {
        0 : '星期一',
        1 : '星期二',
        2 : '星期三',
        3 : '星期四',
        4 : '星期五',
        5 : '星期六',
        6 : '星期天',
        }
        day = datetime.datetime.now().date().weekday()
        # if week_day_dict[day]=='星期六' or week_day_dict[day]=='星期天':
        if week_day_dict[day]=='星期六':
            print('not working days')
            return False
        else:
            return True

    @staticmethod
    #判断是否是9点30到15点交易时间
    def IsWorkingHours():
        d_starttime = datetime.datetime.strptime(str(datetime.datetime.now().date())+'9:30', '%Y-%m-%d%H:%M')
        d_endtime =  datetime.datetime.strptime(str(datetime.datetime.now().date())+'15:00', '%Y-%m-%d%H:%M')
        
        d_midtime_1=datetime.datetime.strptime(str(datetime.datetime.now().date())+'11:30', '%Y-%m-%d%H:%M')
        d_midtime_2=datetime.datetime.strptime(str(datetime.datetime.now().date())+'13:00', '%Y-%m-%d%H:%M')

        n_time = datetime.datetime.now()

        # 判断当前时间是否在范围时间内
        if n_time > d_starttime and n_time<d_endtime:
            if n_time>d_midtime_2 or n_time<d_midtime_1:
                print('交易时间')
                return(True)
            else:
                print('非交易时间')
        else:
            print('非交易时间')
            return(False)

    @staticmethod
    def GetCurrentWorkingDir():
        return os.getcwd()
    
    # @staticmethod

# if __name__=='_main_':
if __name__=='__main__':
    # print(Util.IsTradingDays('2020-07-01'))
    # print(Util.Percent2Float('-1.94%'))

    # print(Util.GetDeltaTradingDate('2020-07-01',delta=3))

    print(Util.GetCloseBeforeTradingDate('2020-08-09'))
    print(Util.GetCloseAfterTradingDate('2020-08-09'))

