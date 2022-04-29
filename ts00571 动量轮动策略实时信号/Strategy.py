# 微信消息接口及其它公共模块接口
# import sys
# sys.path.append('C:\\Users\\Aaron\\Documents\\MyMobileBooks_800_Reading\\MyTSSnippets\\CommonModules')

import config

import datetime
import pandas as pd
from Util import *


# StrategyDL 动量策略
# StrategyG 高成长策略
# StrategyZ 最低市值策略



# 策略基类
class Strategy():
    def __init__(self):
        pass
    pass

# 动量策略类
class StrategyDL(Strategy):

    def __init__(self):
        super(StrategyDL, self).__init__()
        # self.theAccount=Account()

        # 信号的输出用DataFrame表示Index  IndexName N日涨幅
        #   M日均线  当前价格
        # self.dicOutput={}

        self.dfOutput=pd.DataFrame()

        # 打印中间结果输出标签
        self.bPrintFlag=True

        self.CurrentTimePrice=0

        # self.cg_RunTime=''
        self.cg_VRDays=0
        self.cg_AVDays=0
        self.cg_StrategyName=''

        # 策略运行时间
        self.RunTime=''

    def __ReadStrategyParameters(self):
        
        pass
    
    # 获取几日涨幅
    def __GetIndexVR(self,index, thedate,thetime):
         # df_VR = get_bars(index, 
        #                  self.cg_VRDays, 
        #                  unit='1d',
        #                  fields=['date','close'],
        #                  include_now=False,
        #                  end_dt=datetime.datetime.strptime(thedate,'%Y-%m-%d'))

        df_VR=config.g_DataFeeder.GetDayPriceBar(index,self.cg_VRDays,datetime.datetime.strptime(thedate,'%Y-%m-%d'))
        
        if self.bPrintFlag==True: 
            print(df_VR)

        df_VR_rows=df_VR.shape[0]-1
    #     print(df_VR_rows)

        # 计算当前实时涨幅
#         changepercent_VR=(df_VR['close'][df_VR_rows]-df_VR['close'][0])/df_VR['close'][0]

        # ===============主要的计算代码 ======================
        changepercent_VR=(self.CurrentTimePrice-df_VR['close'][0])/df_VR['close'][0]

        if self.bPrintFlag==True: 
            print('=====当前实时值相对' + str(self.cg_VRDays) + '日前涨幅:=====')
           
            print(Util.Float2Percent(changepercent_VR))

        return changepercent_VR

    # 注意：这里取均线值，当日的值不可以用
    # 这里的问题在于不应该取当日的价格，应该只取前一日的为止，今天的用信号判断时间来获取
    def __GetIndexAV(self,index, thedate,thetime):
     
        # df_AV=config.g_DataFeeder.GetDayPriceBar(index,self.cg_AVDays,datetime.datetime.strptime(thedate,'%Y-%m-%d'))

        YesterdayDateTime=Util.DateDelta(thedate, -1)

        df_AV=config.g_DataFeeder.GetDayPriceBar(index,int(self.cg_AVDays)-1,datetime.datetime.strptime(thedate,'%Y-%m-%d'))

        df_AV.sort_values(by='date', inplace=True, ascending=False)
        
        if self.bPrintFlag==True: 
            print(df_AV)

        df_AV_rows=df_AV.shape[0]
        # print(df_AV_rows)

        # ===============主要的计算代码 ======================
        averageprice=(self.CurrentTimePrice+df_AV['close'].sum())/(df_AV_rows+1)

        # changepercent_AV=(self.CurrentTimePrice-averageprice)/self.CurrentTimePrice
        changepercent_AV=(self.CurrentTimePrice-averageprice)/averageprice

        if self.bPrintFlag==True: 
            print('=====当前实时值相对' + str(self.cg_AVDays) + '日均线差值百分值:=====')
            # print("%.2f%%" % (changepercent_AV * 100))
            print(Util.Float2Percent(changepercent_AV))

        return changepercent_AV

    #   获取单个指数的涨幅、均线差值比
    #   注意：回测时输入的日期和时间，不可以用当日的close价格
    def __GetIndexVR_AV(self,index,thedate,thetime):
        
        # 判断是否是实时模式，如果是，用JQData, 不是的话，用LocalData
        
        self.CurrentTimePrice=float(config.g_DataFeeder.GetTheDateTimeMinute10Price(index,thedate,thetime))

        if self.bPrintFlag==True:         
            print('当前价格:' + str(self.CurrentTimePrice) )

        changepercent_VR=self.__GetIndexVR(index, thedate,thetime)

        changepercent_AV=self.__GetIndexAV(index, thedate,thetime)
        
        # 不能用百分号，否则形成字符串，无法进行比较排序
        # return "%.2f%%" % (changepercent_VR * 100),"%.2f%%" % (changepercent_AV * 100)
        return changepercent_VR,changepercent_AV 


    # # 获取一个策略中的最佳标的
    # # 用于单次交互查询模式
    # def GetBestIndex(self,thedate, thetime):
    #     dicVR=dict()
    #     dicAV=dict()
        
    #     if thedate=='':
    #         thedate=datetime.datetime.today().strftime('%Y-%m-%d')
        
    #     if thetime=='':
    #         thetime=time.strftime("%H:%M:%S", time.localtime()) 

      
    #     for ETF in self.ETFList:
    #         print('============')
    #         print(ETF + ' ' + self.ETFList[ETF])
    #         print('============')

    #         listVR_AV=self.GetIndexVR_AV(ETF, thedate, thetime)

    #         dicVR[ETF]=float(listVR_AV[0])
    #         dicAV[ETF]=float(listVR_AV[1])

    #     if g_silentmode==False:
    #         print('dicVR:')
    #         print(dicVR)

    #     d_order=sorted(dicVR.items(),key=lambda x:x[1],reverse=True)
    #     # dicVR.sort(key=lambda x:x[1],reverse=True)
    #     # d_order=dicVR
    #     # print('d_order_Sorted:')
    #     # print(d_order)

    #     print('===================' +self.cg_StrategyName + ' 信号==================')
    #     # if(float(dicAV[d_order[0]].strip('%'))>0):
    #     if(dicAV[d_order[0][0]]>0):
    #         print('涨幅最大标的：' + str(d_order[0][0]) + ' ' + self.ETFList[str(d_order[0][0])])

    #         ShowPct_VR="%.2f%%" % (dicVR[d_order[0][0]] * 100)

    #         ShowPct_AV="%.2f%%" % (dicAV[d_order[0][0]] * 100)

    #         print(str(self.cg_VRDays) + '日涨幅：' + str(ShowPct_VR))
    #         print(str(self.cg_AVDays) +'日均线差值：'+ str(ShowPct_AV))

    #     else:
    #         print('=========所有标的都在均线以下，全部卖出========')
    #         for ETF in self.ETFList:

    #             ShowPct_VR="%.2f%%" % (dicVR[ETF] * 100)

    #             ShowPct_AV="%.2f%%" % (dicAV[ETF] * 100)

    #             # print(ETF + ' ' + self.ETFList[ETF] + ':' + dicVR[ETF] + ';' + dicAV[ETF] )
    #             print(ETF + ' ' + self.ETFList[ETF] + ':' + ShowPct_VR  + ';' + ShowPct_AV )
    #         print('====================================================')
    #     return 0
    
    
    # 用于实时监控模式、回测模式
    # 获取当前信号，根据当前持仓决定买入、卖出
    # 如果买入信号，读取持仓，如果空仓则买入，写入日志
    # 如果卖出信号，读取持仓，如果有则卖出，写入日志
    # def Transaction(self, theDate,theTime):

    #     # 算法===============
    #     # GetSignal()

    #     # ReadPosition()

    #     # 进行买卖操作，并做记录：
    #     # 如果已有仓位，
    #     # 如果目前空仓，
    #     # Transact()

    #     # WriteLogger()

    #     # 获取信号BUY or SELL、买入卖出标的
    #     # 数据格式 BUY,000300.XSHG或者SELL,ALL
    #     Signal,SelectedIndex=self.theStrategy.GetTransactionSignal(theDate, theTime)

    #     # 读取当前持仓状态
    #     CurrentPosition=self.theAccount.ReadPosition()

    #     #如果当前持仓
    #     if CurrentPosition!='EMPTY':
            
    #         PositionIndex,PositionShares=CurrentPosition
    #         PositionShares=1000
    #         if Signal=='SELL':
    #             if PositionIndex==SelectedIndex:
    #                 self.theAccount.Transact('SELL',SelectedIndex,PositionShares)
    #             else:
    #                 print('需要卖出的和现有仓位不符。请检查')

    #         elif Signal=='BUY':

    #             print('当前已持仓，不需买入')

    #     #如果当前空仓
    #     else:
            
    #         if Signal=='BUY':
    #             self.theAccount.Transact('BUY',SelectedIndex,1000)

    #         elif Signal=='SELL':
    #             print('当前无仓位，无需卖出')            

    # 在实时循环模式进行获取最优Index，然后操作
    # 返回值：BUY,index,Price；SELL,ALL,0
    # 关键算法
    def GetTransactionSignal(self,thedate, thetime):
        # dicVR=dict()
        # dicAV=dict()
        
        if thedate=='':
            thedate=datetime.datetime.today().strftime('%Y-%m-%d')
        
        if thetime=='':
            thetime=time.strftime("%H:%M:%S", time.localtime()) 

        iDFRow=0

        VRColumnName=str(self.cg_VRDays)+ '日涨幅'
        AVColumnName='当前价格相对'+ str(self.cg_AVDays)+ '日均值差值'

        # 主循环，对每个ETF获取某天、某时的涨幅变动、相对均值的数值百分比
        for ETF in self.ETFList:
            if self.bPrintFlag==True: 
                print('============')
                print(ETF + ' ' + self.ETFList[ETF])
                print('============')

            VR_AV=self.__GetIndexVR_AV(ETF, thedate, thetime)

            # 输出结果
            self.dfOutput.loc[iDFRow,'Index']=ETF
            self.dfOutput.loc[iDFRow,'IndexName']=config.g_DataFeeder.GetSecurityName(self.dfOutput.loc[iDFRow,'Index'])
            self.dfOutput.loc[iDFRow,VRColumnName]=round(VR_AV[0],5) # Util.Float2Percent(VR_AV[0]) #"%.2f%%" % (VR_AV[0]* 100)
            self.dfOutput.loc[iDFRow,AVColumnName]=round(VR_AV[1],5) # Util.Float2Percent(VR_AV[1]) #"%.2f%%" % (VR_AV[1]* 100)

            iDFRow=iDFRow+1

            # dicVR[ETF]=listVR_AV[0]
            # dicAV[ETF]=listVR_AV[1]

        # print('排序前：')
        # print(self.dfOutput)

        self.dfOutput.sort_values(VRColumnName,ascending=False,inplace=True)# 按照涨幅排序

        # 为什么要这句？
        # 因为排序后，第一列的索引被打乱，要将第一列的索引重新置换为0到n的顺序
        self.dfOutput.reset_index(drop=True, inplace=True)

        # print('排序后：')
        if self.bPrintFlag==True: 
            print(self.dfOutput)

        # 根据涨幅进行排序
        # d_order=sorted(dicVR,key=lambda x:x[1],reverse=True)

        # if g_silentmode==False:
        #     print('dicVR:')
        #     print(dicVR)

        # d_order=sorted(dicVR.items(),key=lambda x:x[1],reverse=True)

        if self.bPrintFlag==True: 
            print('==============' + self.cg_StrategyName + '============')

        # if(dicAV[d_order[0][0]]>0):
        # 这里是关键步骤，除了判断第一位是否2个指标都大于0，还要判断和前一天比较，是否过大（如超过2%，不要买，换第二个）；以及是否连续上涨了几天（如是则不要买入）？
        if self.dfOutput.loc[0,VRColumnName]>0 and self.dfOutput.loc[0,AVColumnName]>0:
            if self.bPrintFlag==True: 
                # print('涨幅最大标的：' , str(d_order[0][0])  , self.ETFList[str(d_order[0][0])])
                print('涨幅最大标的：', str(self.dfOutput.loc[0,'IndexName']))

            # ShowPct_VR="%.2f%%" % (dicVR[d_order[0][0]] * 100)

            # ShowPct_AV="%.2f%%" % (dicAV[d_order[0][0]] * 100)

            # ShowPct_VR="%.2f%%" % (self.dfOutput.loc[0,VRColumnName]* 100)

            # ShowPct_AV="%.2f%%" % (self.dfOutput.loc[0,AVColumnName] * 100)

            # IndexPrice=g_DataFeeder.GetTheDateTimePrice(str(d_order[0][0]),thedate,thetime)
            # IndexPrice=config.g_DataFeeder.GetTheDateTimeMinute10Price(str(dfOutput.loc[0,'Index'],thedate,thetime)

            SelectedIndexPrice=float(config.g_DataFeeder.GetTheDateTimeMinute10Price(self.dfOutput.loc[0,'Index'],thedate,thetime))

            if self.bPrintFlag==True:
                print(str(self.cg_VRDays) ,'日涨幅：' , self.dfOutput.loc[0,VRColumnName])
                print(str(self.cg_AVDays) ,'日均线差值：',self.dfOutput.loc[0,AVColumnName])


                print(thedate, thetime, ': BUY', self.dfOutput.loc[0,'Index'],str(self.dfOutput.loc[0,'IndexName']),SelectedIndexPrice)

            # return 'BUY', dfOutput.loc[0,'Index'], IndexPrice #包括Index及价格 
            return 'BUY', self.dfOutput.loc[0,'Index'], SelectedIndexPrice#包括Index及价格
        else:
            
            if self.bPrintFlag==True: 

                print(thedate, thetime,'=========排名第一的标的涨幅或均线差为负========')

                # 输出统一结果
                # print('====================================================')
            # print('SELL', 'ALL', '0')
            return 'SELL','ALL','0'

        # 输出结果，包括其它的涨跌幅
        # for ETF in self.ETFList:

        #     ShowPct_VR="%.2f%%" % (dicVR[ETF] * 100)

        #     ShowPct_AV="%.2f%%" % (dicAV[ETF] * 100)

        #     # print(ETF + ' ' + self.ETFList[ETF] + ':' + dicVR[ETF] + ';' + dicAV[ETF] )
        #     if self.bPrintFlag==True: 
        #         print(ETF,self.ETFList[ETF], ':' , ShowPct_VR  , ';' , ShowPct_AV )
    
        
# 策略_中国指数
class StrategyDL010(StrategyDL):

    def __init__(self):
        #默认值
        super(StrategyDL010, self).__init__()
        self.ETFList = {
            
            '000016.XSHG':'上证50',
            '000300.XSHG':'沪深300',
            '399006.XSHE': '创业板',
            '000905.XSHG':'中证500'
            }
            
        self.cg_VRDays=13
        self.cg_AVDays=5
        self.cg_StrategyName='中国宽基指数策略'
        
        # 持仓保存路径
        # self.theAccount.PositionFileSavePath='StrategyPosition_010.csv'

        # 日志保存路径
        # self.LoggerFileSavePath='StrategyLogger_010.csv'

# 策略_环球指数
class StrategyDL020(StrategyDL):

    def __init__(self):
        super(StrategyDL020, self).__init__()
        #默认值
        self.ETFList = {
            # '513030.XSHG':'德国30ETF',
            '513100.XSHG':'纳指ETF',
            # '513520.XSHG': '日经ETF',
            # '518880.XSHG':'黄金ETF',
            '000300.XSHG':'沪深300'
            }
        self.cg_VRDays=13
        self.cg_AVDays=5
        self.cg_StrategyName='环球指数ETF策略'
        
        # 持仓保存路径
        # self.theAccount.PositionFileSavePath='StrategyPosition_020.csv'

        # 日志保存路径
        # self.LoggerFileSavePath='StrategyLogger_020.csv'

# 策略_行业指数
class StrategyDL030(StrategyDL):

    def __init__(self):
        super(StrategyDL030, self).__init__()
        self.ETFList = {'399417.XSHE':'新能源车',
            '399932.XSHE':'消费',
            '399967.XSHE':'军工',
            '399975.XSHE':'证券',
            '399971.XSHE':'传媒',
            '399987.XSHE':'酒',
            '515070.XSHG':'人工智能',
            '515000.XSHG':'科技龙头',
            '512480.XSHG':'半导体',
            '512800.XSHG':'银行',
            '512200.XSHG':'房地产'
            }
        self.cg_VRDays=13
        self.cg_AVDays=5
        self.cg_StrategyName='行业ETF策略'

        # 持仓保存路径
        # self.theAccount.PositionFileSavePath='StrategyPosition_010.csv'

        # 日志保存路径
        # self.LoggerFileSavePath='StrategyLogger_030.csv'


# 高成长策略
class StrategyG():

    def __init__(self):
        pass

# 高成长策略
class StrategyG010(StrategyG):

    def __init__(self):
        pass

# 最低市值策略
class StrategyZ():
    # 最低市值策略
    def __init__(self):
        pass

# 最低市值策略
class StrategyZ010(StrategyZ):

    def __init__(self):
        pass