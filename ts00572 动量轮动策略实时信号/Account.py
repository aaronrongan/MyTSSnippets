
import config

import os

import glob

import Util

import time

# 账户，实体类，放入策略类，作为策略的一个属性
class Account():
    def __init__(self):
        # # 本金
        # self.Capital=0 

        # # 目前资金
        # self.Cash=0

        # 目前代码及持仓数（暂时只有一个，以后扩充为多个）,ETF：持仓数
        self.Position={}

        # 持仓保存文件路径（不含文件名）
        self.PositionFileSavePath=''

        # 持仓保存名称，如StrategyPosition_010.csv
        self.PositionFileName=''

        # 交易日志保存路径（不含文件名）
        self.TransLoggerFileSavePath=''

        # 交易日志保存路径（不含文件名），如StrategyTransLogger_010.csv
        self.TransLoggerFileName=''

        # 每日记录保存路径（不含文件名）
        self.DailyLoggerFileSavePath=''

        # 每日记录保存路径（不含文件名），如StrategyDailyLogger_010.csv
        self.DailyLoggerFileName=''
    
    # 获取当前持仓
    # 返回格式：000300.XSHG, 1000
    def ReadPosition(self):

        # pwd = os.getcwd()

        # print('ReadPosition:' + pwd)

        # 文件读取错误处理
        while(1):
            try:
                with open(self.PositionFileSavePath + self.PositionFileName ) as file_obj:
                # file_obj=open(pwd +'/' + HoldingFileSavePath)
                    # time.sleep(0.5)
                    lines = file_obj.readlines()
                
                break

            except Exception as e:
                print('文件读取错误:'+ self.PositionFileSavePath + self.PositionFileName)
                print('exception:' + str(e))
            
                time.sleep(1)
                print('文件读取错误，等待1秒。。。')
                # exit()

        # finally:
        #     file_obj.close()
             

        if lines!=[]:
            thedate=lines[0].split(',')[0]
            thetime=lines[0].split(',')[1]
            signal=lines[0].split(',')[2]
            index=lines[0].split(',')[3]
            shares=lines[0].split(',')[4]
            price=lines[0].split(',')[5]
            return thedate,thetime,signal,index,shares,price
        else:
            return 'EMPTY','EMPTY','EMPTY','EMPTY','ALL',0
    

    # 买卖操作
    def Transact(self,theDate,theTime, Signal,Index,Shares,Price):

        # 下单操作
        self.PlaceOrder(theDate,theTime,Signal,Index,Shares,Price)

        # 做记录:当前仓位
        self.WritePosition(theDate,theTime,Signal,Index,Shares,Price)

        # 做记录:日记及买卖记录
        self.WriteLogger(theDate,theTime,Signal, Index,Shares,Price)

    # 下单信号
    # 目前发送短信、微信、邮件
    def PlaceOrder(self,theDate,theTime, Signal,Index,Shares,Price):
        
        IndexName=config.g_DataFeeder.GetSecurityName(Index)
        Message=theDate + ' ' + theTime + ' ' + Signal + ' ' + Index + ' ' +  IndexName + '' + str(Shares) +' ' + str(Price)

        # Util.SendMail(Message)
        
        if config.g_WechatSwitchOn==True: 
            config.g_wechat.SendWeChatMessage(Message)  
            # print('WeChat SendMessage')
            # Util.SendPhoneMessage(Message)

    # 写入当前持仓
    # 将信号写入本地文件，当前持仓状态，何时买入卖出
    # 格式：000300.XSHG, 1000
    def WritePosition(self,theDate,theTime, Signal, Index,Shares,Price):
        # print('WritePosition:')
        pwd = Util.Util.GetCurrentWorkingDir()

        # print('WritePosition:' + pwd)

        # currentDate=datetime.datetime.today().strftime('%Y-%m-%d')
        # currentTime=time.strftime("%H:%M:%S", time.localtime()) 

        try:
            with open(self.PositionFileSavePath + self.PositionFileName,'w' ) as file_obj:
                if Signal=='BUY':
                
                    # lines = file_obj.readlines()
                    # file_obj.writelines(currentDate + ','+currentTime +
                    #                     ',' + Signal +','+ Index + ',' + Shares)
                    file_obj.writelines(theDate + ',' + theTime +',' + Signal + ',' + Index + ',' + str(Shares)+','+ str(Price))
                elif Signal=='SELL':
                # 卖出时持仓文件清空
                # with open(self.PositionFileSavePath + self.PositionFileName,'w' ) as file_obj:
                    file_obj.writelines('')
                
        finally:
            # if file_obj!=None:
            # file_obj.close()
            pass

    

    # 设置持仓文件名
    def SetPositionFileName(self,name):
        self.PositionFileName='StrategyPosition_' + name +'.csv'

    # 清理之前的Position文件
    def CleanPositionFile(self,StrategyID):
        # clean_list = os.listdir(self.PositionFileSavePath)
        # for filename in clean_list:
        #     file_path = os.path.join(self.TransLoggerFileSavePath, filename)
        #     if os.path.isfile(file_path):
        #         # os.remove(file_path)
        #         # 打开然后清空一个文件
        #         open('file.txt', 'w').close()

        os.chdir(self.PositionFileSavePath)
        # for file in glob.glob('*Position*'):
        for file in glob.glob('*' + self.PositionFileName +'*'):
            self.PositionFileName
            open(file, 'w').close()

    # 设置持仓文件名
    def SetTransLoggerFileName(self,name):
        self.TransLoggerFileName='StrategyTransLogger_' + name +'.csv'

    # 设置持仓文件名，对于Logger文件，需要动态创建
    def CreateTransLoggerFile(self,StrategyID,ParameterList):

        thedatetime=Util.Util.GetShortDateTime()

        self.TransLoggerFileName='StrategyTransLogger_' + StrategyID + '_'+thedatetime +'.csv'

        with open(os.path.join(self.TransLoggerFileSavePath,self.TransLoggerFileName),'w') as file_obj:
            file_obj.writelines('StrategyID:' + StrategyID)
            file_obj.writelines('\n')

            file_obj.writelines('RunTime:'+ str(ParameterList[0]))
            file_obj.writelines('\n')

            file_obj.writelines('VRDate:'+ str(ParameterList[1]))
            file_obj.writelines('\n')

            file_obj.writelines('AVDate:'+str(ParameterList[2]))
            file_obj.writelines('\n')

            file_obj.writelines('Date,Time,Signal,Index,Shares,Price,CurPL,CumPL')
            file_obj.writelines('\n')

    # 写交易记录和每日状态
    def WriteLogger(self,theDate,theTime,Signal, Index,Shares,Price):
        
        self.__WriteTransLogger(theDate,theTime,Signal, Index,Shares,Price)
        # self.__WriteDailyLogger(startdate,enddate)

    # 写入当前操作记录，并且有每次的盈利记录
    # 将何时买入卖出写入本地文件
    # 格式：2020-07-16,15:00:00,SELL,000300.XSHG,1000,12.34
    def __WriteTransLogger(self,theDate,theTime,Signal, Index,Shares,Price):
        # print('WriteLogger:')

        # pwd=Util.GetCurrentWorkingDir()
        # print('WriteLogger:'+ pwd )

        # currentDate=datetime.datetime.today().strftime('%Y-%m-%d')
        # currentTime=time.strftime("%H:%M:%S", time.localtime()) 

        
        # 判断文件如果为空，则写入标题栏
        with open(self.TransLoggerFileSavePath + self.TransLoggerFileName,'r+' ) as file_obj:
            # mLines = file_obj.readlines()
            if os.path.getsize(os.path.join(self.TransLoggerFileSavePath , self.TransLoggerFileName))==0:
                # file_obj.writelines('Date,Time,Signal,Index,Shares,Price,CurPL,CumPL')
                # file_obj.writelines('\n')
                pass

            # 如果是第一行并且为BUY，CurPL=1, CumPL=1
            # Buy行，CurPL、CumPL是上一行数据，SELL行，CurPL
            # 读取上一行
            else:
                mLines = file_obj.readlines()
                # print(mLines)

                # 第一笔交易记录
                if len(mLines)==5:
                    file_obj.writelines(theDate + ','+theTime +',' + Signal +','+ Index + ',' + str(Shares)+','+str(Price) + ',' + '1' + ',' + '1')
                    file_obj.writelines('\n')

                elif len(mLines)>5:
                    
                    # # 取最后一行，去除\n
                    lastline=mLines[-1].replace('\n', '')
                    # print('lastline:' + lastline)

                    lastPrice=round(float(lastline.split(',')[-3]),5)
                    # print(lastline.split(',')[-3])

                    lastCurPL=round(float(lastline.split(',')[-2]),5)
                    # print(lastline.split(',')[-2])

                    # print('lastCurPL:' + str(lastCurPL))
                    
                    lastCumPL=round(float(lastline.split(',')[-1]),5)
                    # print('lastCumPL:' + str(lastCumPL))

                    if Signal=='BUY':
                        thisCurPL=1
                        thisCumPL=lastCumPL

                    elif Signal=='SELL':
                        thisCurPL=round(Price/lastPrice,5)
                        thisCumPL=round(lastCumPL*thisCurPL,5)

                    file_obj.writelines(theDate + ','+theTime +
                                            ',' + Signal +','+ Index + ',' + str(Shares)+','+str(Price)+','+str(thisCurPL) +',' +str(thisCumPL))

                    file_obj.writelines('\n')
            # print('')

    

    # 对于最后一天，完成日志，即卖出清仓。如果仍然持仓，加入最后一行
    # 对回测模式
    def FinishTransLogger(self,theDate):
        with open(self.TransLoggerFileSavePath + self.TransLoggerFileName,'r+' ) as file_obj:
            mLines = file_obj.readlines()
            # print(mLines)

            if len(mLines)>2:
                # 取最后一行，去除\n
                lastline=mLines[-1].replace('\n', '')
                # print('lastline:' + lastline)
                
                LastSignal=lastline.split(',')[2]

                if LastSignal=='BUY':
                    lastIndex=lastline.split(',')[3]

                    lastPrice=round(float(lastline.split(',')[-3]),5)
                        
                    lastCurPL=round(float(lastline.split(',')[-2]),5)
                
                    lastCumPL=round(float(lastline.split(',')[-1]),5)

                    # CurrentPrice=g_DataFeeder.GetDayPriceBar(lastIndex,1,theDate)['close'][0]
                    CurrentPrice=config.g_DataFeeder.GetTheDateTimeMinute10Price(lastIndex,theDate,'15:00:00')
                   

                    thisCurPL=round(CurrentPrice/lastPrice,5)
                    thisCumPL=round(lastCumPL*thisCurPL,5)

                    file_obj.writelines(str(theDate) + ','+ '15:00:00' +
                                            ',' + 'SELL' +','+ lastIndex + ',' + str(100)+','+str(CurrentPrice)+','+str(thisCurPL) +',' +str(thisCumPL))

                    file_obj.writelines('\n')
                elif LastSignal=='SELL':
                    # if self.bPrintFlag==True:
                    #     print('已清仓')
                    pass

    


# Trading_BackTest账户，实体类
# 和RealTime账户的区别：
#   文件保存地址不一样
class Account_BackTest(Account):
    def __init__(self):
        super().__init__()

        pwd = os.getcwd()

        # 持仓保存文件路径（不含文件名）
        self.PositionFileSavePath=config.g_Data_BackTest #pwd +'/Data_BackTest/'

        # 日志保存路径（不含文件名）
        self.TransLoggerFileSavePath=config.g_Data_BackTest #pwd +'/Data_BackTest/'

        # BackTest前将所有的回测Logger文件删除
        # __CleanAllLoggerFiles()

        # BackTest前将所有的回测Position文件清空
        self.__CleanAllPositionFiles()

    # 清理之前的Position文件
    def __CleanAllPositionFiles(self):
        # clean_list = os.listdir(self.PositionFileSavePath)
        # for filename in clean_list:
        #     file_path = os.path.join(self.TransLoggerFileSavePath, filename)
        #     if os.path.isfile(file_path):
        #         # os.remove(file_path)
        #         # 打开然后清空一个文件
        #         open('file.txt', 'w').close()

        os.chdir(self.PositionFileSavePath)
        for file in glob.glob('*Position*'):
            # print(file)
            # 打开然后清空一个文件
            open(file, 'w').close()
    
    # 删除之前的Position文件
    def __RemoveAllPositionFiles(self):
        clean_list = os.listdir(self.PositionFileSavePath)
        for filename in clean_list:
            file_path = os.path.join(self.TransLoggerFileSavePath, filename)
            if os.path.isfile(file_path):
                # os.remove(file_path)
                # 打开然后清空一个文件
                open('file.txt', 'w').close()

    # 将Logger文件删除
    # 似乎用不到
    # 这里的错误：没有搜出含
    def __CleanAllLoggerFiles(self):
        # del_list = os.listdir(self.TransLoggerFileSavePath)
        # for filename in del_list:
        #     file_path = os.path.join(self.TransLoggerFileSavePath, filename)
        #     if os.path.isfile(file_path):
        #         os.remove(file_path)
        os.chdir(self.PositionFileSavePath)
        for file in glob.glob('*Logger*'):
            # print(file)
            # 删除文件
            os.remove(file)

    # def CreateTransLoggerFiles(self,TransLoggerFileName):
    # 获取当前Account的交易记录日志文件
    def GetTransLoggerFilePathName(self): 
        return os.path.join(self.TransLoggerFileSavePath,  self.TransLoggerFileName)

     # def CreateTransLoggerFiles(self,TransLoggerFileName):
    # 获取当前Account的交易记录日志文件
    def GetDailyLoggerFilePathName(self):
        return os.path.join(self.TransLoggerFileSavePath,  self.TransLoggerFileName)
    


# RealTime账户，实体类，
# 和BackTest账户的区别：
#   文件保存地址不一样
class Account_RealTime(Account):
    def __init__(self):
        super().__init__()

        pwd = os.getcwd()

        # 持仓保存文件路径（不含文件名）
        self.PositionFileSavePath=config.g_Data_RealTime #pwd +'/Data_RealTime/'

        # 日志保存路径（不含文件名）
        self.TransLoggerFileSavePath=config.g_Data_RealTime # pwd +'/Data_RealTime/'
    

# Trading_Optimizer账户，实体类

class Account_Optimizer(Account):
    def __init__(self):
        super().__init__()

        pwd = os.getcwd()

        # 持仓保存文件路径（不含文件名）
        self.PositionFileSavePath= config.g_Data_Optimizer  # pwd +'/Data_Optimizer/'

        # 日志保存路径（不含文件名）
        self.TransLoggerFileSavePath=config.g_Data_Optimizer # pwd +'/Data_Optimizer/'

        # BackTest前将所有的回测Logger文件删除
        # __CleanAllLoggerFiles()

        # BackTest前将所有的回测Position文件清空
        self.__CleanAllPositionFiles()

    # 清理之前的Position文件
    def __CleanAllPositionFiles(self):
        # clean_list = os.listdir(self.PositionFileSavePath)
        # for filename in clean_list:
        #     file_path = os.path.join(self.TransLoggerFileSavePath, filename)
        #     if os.path.isfile(file_path):
        #         # os.remove(file_path)
        #         # 打开然后清空一个文件
        #         open('file.txt', 'w').close()

        os.chdir(self.PositionFileSavePath)
        for file in glob.glob('*Position*'):
            # print(file)
            # 打开然后清空一个文件
            open(file, 'w').close()
    
    # 删除之前的Position文件
    def __RemoveAllPositionFiles(self):
        clean_list = os.listdir(self.PositionFileSavePath)
        for filename in clean_list:
            file_path = os.path.join(self.TransLoggerFileSavePath, filename)
            if os.path.isfile(file_path):
                # os.remove(file_path)
                # 打开然后清空一个文件
                open('file.txt', 'w').close()

    # 将Logger文件删除
    # 似乎用不到
    # 这里的错误：没有搜出含
    def __CleanAllLoggerFiles(self):
        # del_list = os.listdir(self.TransLoggerFileSavePath)
        # for filename in del_list:
        #     file_path = os.path.join(self.TransLoggerFileSavePath, filename)
        #     if os.path.isfile(file_path):
        #         os.remove(file_path)
        os.chdir(self.PositionFileSavePath)
        for file in glob.glob('*Logger*'):
            # print(file)
            # 删除文件
            os.remove(file)

    # def CreateTransLoggerFiles(self,TransLoggerFileName):
    # 获取当前Account的交易记录日志文件
    def GetTransLoggerFilePathName(self):
        return os.path.join(self.TransLoggerFileSavePath,  self.TransLoggerFileName)
    
    
    # 获取当前Account的交易记录日志文件
    def GetDailyLoggerFilePathName(self):
        return os.path.join(self.DailyLoggerFileSavePath,  self.DailyLoggerFileName)

    # 设置持仓文件名，对于Logger文件，需要动态创建
    # 对于优化，不能用生成文件的方法，否则太慢
    # def CreateTransLoggerFile(self,StrategyID,ParameterList):

    #     thedatetime=Util.Util.GetShortDateTime()

    #     self.TransLoggerFileName='StrategyTransLogger_' + StrategyID + '_'+thedatetime +'.csv'

    #     with open(os.path.join(self.TransLoggerFileSavePath,self.TransLoggerFileName),'w') as file_obj:
    #         file_obj.writelines('StrategyID:' + StrategyID)
    #         file_obj.writelines('\n')

    #         file_obj.writelines('RunTime:'+ str(ParameterList[0]))
    #         file_obj.writelines('\n')

    #         file_obj.writelines('VRDate:'+ str(ParameterList[1]))
    #         file_obj.writelines('\n')

    #         file_obj.writelines('AVDate:'+str(ParameterList[2]))
    #         file_obj.writelines('\n')

    #         file_obj.writelines('Date,Time,Signal,Index,Shares,Price,CurPL,CumPL')
    #         file_obj.writelines('\n')