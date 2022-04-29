# 测试代码 test00572 snapbaiyunfei-selenium


import requests
# import unittest
from bs4 import BeautifulSoup

import urllib3
from selenium import webdriver
import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys

from selenium.webdriver.common.action_chains import ActionChains

import socket

import pandas as pd

import sys
import os
import lxml

import urllib
import random   #随机生成休眠时间
import time

from requests.adapters import HTTPAdapter

import datetime

from IPython.display import clear_output

import smtplib
from email.mime.text import MIMEText
from email.header import Header

from twilio.rest import Client
import time

# import only system from os 
from os import system, name 


# from easydl import clear_output

url='http://17fx.net/F2020/b_follow.aspx'

urllogin='http://17fx.net/F2020/login.aspx'

hostname=socket.gethostname()
if hostname=='MyWorkstation':
    profileDir = "C:/Users/Aaron/AppData/Roaming/Mozilla/Firefox/Profiles/yn80ouvt.default" #用于MYWorkStation
elif hostname=='MyMacWin10':
    profileDir = "C:/Users/Aaron/AppData/Roaming/Mozilla/Firefox/Profiles/ewg4x7y5.default-release" #用于MyMacwin
elif hostname=='PLRWorkstation':
    profileDir = "C:/Users/Administrator/AppData/Roaming/Mozilla/Firefox/Profiles3n0dd184.default-release" #用于PLRWorkstation
elif hostname=="DESKTOP-DEFM935":
    a=1
    
    
# profile =webdriver.FirefoxProfile(profileDir)
# driver = webdriver.Firefox(profile)
# driver.implicitly_wait(5)


global bDayFirstLogin
global bNewWorkingDay
global dateCurrentDay
global sVIEWSTATE
global sVALIDATION

bDayFirstLogin=True
bNewWorkingDay=True
dateCurrentDay=time.strftime("%Y-%m-%d",time.localtime(time.time()))

#DebugMode: 决定是否发出邮件、发送手机信息
debugmode=False

sCurrentHoldingFullPath=''

def SendMessage(message):
    # Your Account SID from twilio.com/console
    account_sid = "AC412d0f21432ea42fe2f9068b7a26fd35"
    # Your Auth Token from twilio.com/console
    auth_token  = "7c996ef074f8ddbdf5fe200333a41c9c"
    
    client = Client(account_sid, auth_token)

    for each in range(1,2):
        message = client.messages.create(body=message + str(each), from_='+16606754209', to='+8617312656875') 
        time.sleep(1)
        #print(message.sid)
		
		
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

#判断是否是9点到16点
def IsWorkingHours():
    d_time = datetime.datetime.strptime(str(datetime.datetime.now().date())+'9:15', '%Y-%m-%d%H:%M')
    d_time1 =  datetime.datetime.strptime(str(datetime.datetime.now().date())+'15:15', '%Y-%m-%d%H:%M')

    n_time = datetime.datetime.now()

    # 判断当前时间是否在范围时间内

    if n_time > d_time and n_time<d_time1:
        print('ok')
        return(True)
    else:
        print('not in working hours')
        return(False)

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
    if week_day_dict[day]=='星期六' or week_day_dict[day]=='星期天':
        print('not working days')
        return False
    else:
        return True

#判断是否是新日、并且是当日第一次登陆

def IsNewDay(date):
    global dateCurrentDay,bDayFirstLogin
    if date==dateCurrentDay:
        return False
    else:
        dateCurrentDay=date
        bDayFirstLogin=True
        return True

#判断是否是当日第一次登陆
def IsDayFirstLogin():
    global bDayFirstLogin
    if bDayFirstLogin==False:
        return False
    else:
        bDayFirstLogin=False
        return True

def GetViewStateandValidator():
    global sVIEWSTATE, sVALIDATION

    postUrl = 'http://17fx.net/F2020/login.aspx'
    s = requests.Session()  # 为了保存登入信息
    r = s.post(postUrl)
    soup=BeautifulSoup(r.text,'lxml')
    sVIEWSTATE = soup.find('input', id='__VIEWSTATE')['value']
    sVALIDATION = soup.find('input', id='__EVENTVALIDATION')['value']

    return(sVIEWSTATE,sVALIDATION)

#获取当前持仓，currentholding.txt
#Y为有仓位，N为空仓

def GetCurrentHolding():
    pwd = os.getcwd()

    with open(pwd +'/ts00521 白云飞信息自动监控/currentholding.txt') as file_obj:
        lines = file_obj.readlines()
    # print(lines)
    if lines[0]=="N":
        print('当前未持仓')
        return False
    elif lines[0]=="Y":
        print('当前已持仓')
        return True

def WriteSignal(signal):
    pwd = os.getcwd()

    with open (pwd +'/ts00521 白云飞信息自动监控/currentholding.txt',"w") as obj:
        obj.write(signal)

   
#获取买入或卖出交易信号
def GetTransactionSignal():

    sVIEWSTATE,sVALIDATION=GetViewStateandValidator()

    PayloadData  = {'__VIEWSTATE':sVIEWSTATE,
                            '__VIEWSTATEGENERATOR':'CE0712C6',
                            '__EVENTVALIDATION':sVALIDATION,
                            'txt_name_2020_byf': "u457",
                            'txt_pwd_2020_byf': "103889",
                            'btn_login':'登 录'
                            }

    headers1={"User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10.13; rv:55.0) Gecko/20100101 Firefox/55.0"}
    postUrl_real='http://17fx.net/F2020/login.aspx?refurl=http%3a%2f%2f17fx.net%2fF2020%2fb_follow.aspx'  
    # postUrl_real='http://17fx.net/F2020/b_follow.aspx'          
    s = requests.Session()    
    r = s.post(postUrl_real, data=PayloadData, headers=headers1)

    soup=BeautifulSoup(r.text,'lxml')


    # gCurrentUpdateInfo_A7=''
    # gCurrentUpdateInfo_A8=''
    # gCurrentUpdateInfo_A14=''
    # gCurrentUpdateInfo_B2=''
    # gCurrentUpdateInfo_C1=''


    #每个工作日9点时打开1次，发送一次提醒
    # driver.get(urllogin)

    # ht = driver.page_source
    # ht=ht.encode('gb18030').decode('gb18030')

    # soup =BeautifulSoup(ht, 'lxml')

    # sVIEWSTATE = driver.find_element_by_id('__VIEWSTATE').get_attribute('value')
    # sVALIDATION = driver.find_element_by_id('__EVENTVALIDATION').get_attribute('value')

    # print('sVIEWSTATE:' + sVIEWSTATE )
    # print('sVALIDATION:' + sVALIDATION )

    tables=soup.find(class_='content').find_all('table')#.find_all('tbody')
    # print(tables)
    
    #tablenumber=[0,3,6,9,12,15,18,21]
    tablenumber=[0]

    

    for eachnumber in tablenumber:
        
        # print('######## tables[eachnumber] ##########')
        # print(tables[eachnumber])
        # print('################ tables[eachnumber] ##################')

        thetable=tables[eachnumber].find('a').text.strip()

        # print('######## thetable ##########')
        # print(thetable)
        # print('################ thetable ##################')

        # theupdatetime=tables[eachnumber].find('div').text.strip()
        theupdatetime=tables[eachnumber].find('td').text.strip()
        # print('######## theupdatetime ##########')
        # print(theupdatetime)
        # print('################ theupdatetime ##################')
        # print(theupdatetime)

        #对于B1、C2策略，进行策略更新的跟踪
        if eachnumber==0:
            # trs=tables[eachnumber].find_all('tr') #.find('tbody')
            # transactionitem="B1 超高频策略:" + trs[2].text.strip()

            transactionitem="B1 超高频策略:" + theupdatetime

            print('交易信息:' + transactionitem)
#             print('gCurrentUpdateInfo_B2:' + gCurrentUpdateInfo_B2)
            theupdatedate=transactionitem.split('[')[1].split(' ')[0]
            print('交易日期:' + theupdatedate)
            
            # if theupdatedate==today:
                # if gCurrentUpdateInfo_B1 != transactionitem:
            # print('!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
            # print('!!!!!!!!!!!!!!策略B1有更新!!!!!!!!!!!!')
            # print('!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
            # print('SendMesage:')
            # print('######## transactionitem ##########')
            # print(transactionitem)
            # print('################ transactionitem ##################')
             
            # SendMail(transactionitem)
            # SendMessage(transactionitem)
            # gCurrentUpdateInfo_B1=transactionitem
    #                 print('gCurrentUpdateInfo_B2 new:' + gCurrentUpdateInfo_B2)
                # else:
                    # print('')
            if '买入' in  transactionitem:
                # print('SendMessage:买入信号')
                # print(transactionitem)
                # SendMail(transactionitem)
                # SendMessage(transactionitem)
                return 'Buy'
            elif '卖出' in transactionitem:
                # print('SendMessage:卖出信号')
                # print(transactionitem)
                # SendMail(transactionitem)
                # SendMessage(transactionitem)
                return 'Sell'
            else:
                print('No Signal. Please check code.')

        # print(tables[eachnumber])
        # print('##################')
        # print(tables[eachnumber].find_all('div')[1].text.strip())
        # print('##################')
        # thetable=tables[eachnumber].find_all('table')[0]
        # currentholding=thetable.find('td').text.strip()

        thetable=tables[eachnumber].find_all('div')[1].text
        currentholding=thetable.strip()

        # currentholding=thetable.find('td').strip()
        print(currentholding)
        print('#############################################################################')
        print('\n')


#这里无效，因为用到cookie会隔天失效
# headers1={"User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10.13; rv:55.0) Gecko/20100101 Firefox/55.0",
         # 'Cookie': 'Hm_lvt_c6a99d81a6d336a939ba3fd1a08b86a7=1581045329; Hm_lpvt_c6a99d81a6d336a939ba3fd1a08b86a7=1581300116; r%3c%3c%3f%3c=%3d%3eA; %7e%3c%3c%3f%3c=%e6%ae%b7%e5%8b%87'}
		  

# r = requests.get(url,timeout=5,headers=headers1)
# r.close()
# r.text
# print(r.encoding)


# PayloadData  = {'__VIEWSTATE':'/wEPDwUKMTUwNDM4MzczMGRkvsxsVLYbCYoltJ1qRpymQJm6LgITi3Elhvks9Z5u/Dk=',
#                 '__VIEWSTATEGENERATOR':'CE0712C6',
#                 '__EVENTVALIDATION':'/wEdAARod8NymknQo2nJGY/XyVlJzCVMJGnCxB7ZG7bkLlekEsa8wzphH9jstV6K9RvF+kh0OWarNtHZvueomBCnXS0a8APHaPyvDnF5X/JMYJnfeqQoigQDw3s27LsInwLBnpY=',
#                  'txt_name_2020_byf': "u457",
#                  'txt_pwd_2020_byf': "103889",
#                 'btn_login':'登 录'
#                 }





if __name__=="__main__":


    

    sleepseconds1=50
    # gCurrentUpdateInfo_A7=''
    # gCurrentUpdateInfo_A8=''
    # gCurrentUpdateInfo_A14=''
    # gCurrentUpdateInfo_A23=''
    gCurrentUpdateInfo_B1=''
    # gCurrentUpdateInfo_C1=''
    gCurrentUpdateInfo_C2=''
    # gCurrentUpdateInfo_C4=''

    while(1):
        # global sVIEWSTATE, sVALIDATION

        today=time.strftime("%Y-%m-%d",time.localtime(time.time()))
        time_stamp = datetime.datetime.now()

        # print("当前时间：" + time_stamp.strftime('%Y.%m.%d-%H:%M:%S'))
        
        if IsWorkingDays()==False:
            time.sleep(sleepseconds1)
            continue
        else:
            if IsWorkingHours()==False:
            # if IsWorkingHours()==True:
                time.sleep(sleepseconds1)
                continue
            else:

                CurrentSignal=GetTransactionSignal()

                # print('ok')
                # print(sVIEWSTATE)

                #如果持仓
                if GetCurrentHolding()==True:
                    # time.sleep(sleepseconds1)

                    
                    if CurrentSignal=='Sell':
                        # SendMessage('Sell')
                        print('发送卖出信号')

                        if debugmode==False:
                            SendMail('发送卖出信号')
                            SendMessage('发送卖出信号')
                        WriteSignal('N')
                        time.sleep(sleepseconds1)

                        if CurrentSignal=='Buy':
                            print('发送买入信号')
                            if debugmode==False:
                                SendMail('发送买入信号')
                                SendMessage('发送买入信号')
                            WriteSignal('Y')
                            time.sleep(sleepseconds1)
                    elif CurrentSignal=='Buy':
                        print('当前已持仓，无信号')

                #如果空仓
                else:
                    
                    # time.sleep(sleepseconds1)

                    if CurrentSignal=='Buy':
                        print('发送买入信号')
                        SendMail('发送买入信号')
                        SendMessage('发送买入信号')
                        WriteSignal('Y')
                    elif CurrentSignal=='Sell':
                        print('已空仓。不需卖出')

                # if IsNewDay(today):
                    
                

                # if IsDayFirstLogin():
                # bNewWorkingDayFirstLogin=False

            #     PayloadData  = {'__VIEWSTATE':sVIEWSTATE,
            #                     '__VIEWSTATEGENERATOR':'CE0712C6',
            #                     '__EVENTVALIDATION':sVALIDATION,
            #                     'txt_name_2020_byf': "u457",
            #                     'txt_pwd_2020_byf': "103889",
            #                     'btn_login':'登 录'
            #                     }

            #     headers1={"User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10.13; rv:55.0) Gecko/20100101 Firefox/55.0"}
            #     postUrl_real='http://17fx.net/F2020/login.aspx?refurl=http%3a%2f%2f17fx.net%2fF2020%2fb_follow.aspx'  
            #     # postUrl_real='http://17fx.net/F2020/b_follow.aspx'          
            #     s = requests.Session()    
            #     r = s.post(postUrl_real, data=PayloadData, headers=headers1)

            #     soup=BeautifulSoup(r.text,'lxml')


            #     # gCurrentUpdateInfo_A7=''
            #     # gCurrentUpdateInfo_A8=''
            #     # gCurrentUpdateInfo_A14=''
            #     # gCurrentUpdateInfo_B2=''
            #     # gCurrentUpdateInfo_C1=''


            #     #每个工作日9点时打开1次，发送一次提醒
            #     # driver.get(urllogin)

            #     # ht = driver.page_source
            #     # ht=ht.encode('gb18030').decode('gb18030')

            #     # soup =BeautifulSoup(ht, 'lxml')

            #     # sVIEWSTATE = driver.find_element_by_id('__VIEWSTATE').get_attribute('value')
            #     # sVALIDATION = driver.find_element_by_id('__EVENTVALIDATION').get_attribute('value')

            #     print('sVIEWSTATE:' + sVIEWSTATE )
            #     print('sVALIDATION:' + sVALIDATION )

                
            #     tables=soup.find(class_='content').find_all('table')#.find_all('tbody')
            # #     print(tables)
                
            #     #tablenumber=[0,3,6,9,12,15,18,21]
            #     tablenumber=[0,3]

            #     for eachnumber in tablenumber:

            #         thetable=tables[eachnumber].find('a').text.strip()
            #         print(thetable)

            #         theupdatetime=tables[eachnumber].find('div').text.strip()
            #         print(theupdatetime)

            #         #对于B1、C2策略，进行策略更新的跟踪
            #         if eachnumber==0:
            #             trs=tables[eachnumber].find_all('tr') #.find('tbody')
            #             transactionitem="B1 超高频策略:" + trs[2].text.strip()
            # #             print('transactionitem:' + transactionitem)
            # #             print('gCurrentUpdateInfo_B2:' + gCurrentUpdateInfo_B2)
            #             theupdatedate=transactionitem.split('[')[1].split(' ')[0]
            #             print(theupdatedate)
                        
            #             if theupdatedate==today:
            #                 if gCurrentUpdateInfo_B1 != transactionitem:
            #                     print('!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
            #                     print('!!!!!!!!!!!!!!策略B1有更新!!!!!!!!!!!!')
            #                     print('!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
            #                     print(transactionitem) 
            #                     # SendMail(transactionitem)
            #                     # SendMessage(transactionitem)
            #                     gCurrentUpdateInfo_B1=transactionitem
            #     #                 print('gCurrentUpdateInfo_B2 new:' + gCurrentUpdateInfo_B2)
            #                 else:
            #                     print('')
                    

            #         if eachnumber==18:
            #             trs=tables[eachnumber].find_all('tr') #.find('tbody')
            #             transactionitem="C2 低频策略:" + trs[2].text.strip()
            # #             print('transactionitem:' + transactionitem)
            # #             print('gCurrentUpdateInfo_C1:' + gCurrentUpdateInfo_C1)
                    
            #             if gCurrentUpdateInfo_C1 != transactionitem:
            #                 print('!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
            #                 print('!!!!!!!!!!!!!!策略C2有更新!!!!!!!!!!!!')
            #                 print('!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
            #                 print(transactionitem) 
            # #                 SendMail(transactionitem)
            # #                 SendMessage(transactionitem)
            #                 gCurrentUpdateInfo_C1=transactionitem

                    # thetable=tables[eachnumber].find_all('table')[1]
                    # currentholding=thetable.find('td').text.strip()
                    # print(currentholding)
                    # print('#############################################################################')
                    # print('\n')
                
        #将输出栏清空
        # sys.stdout.flush()
        print("当前时间：" + time_stamp.strftime('%Y.%m.%d-%H:%M:%S'))
        time.sleep(sleepseconds1)
        ##clear_output() for Jupyter clear output
        # os.system('cls')
    

# def SnapStrategypage(gCurrentUpdateInfo_B2,gCurrentUpdateInfo_C1):
# while(1):

    # time_stamp = datetime.datetime.now()
    # print("当前时间：" + time_stamp.strftime('%Y.%m.%d-%H:%M:%S'))
	
    # tables=soup.find(class_='content').find_all('table')#.find_all('tbody')
    ##print(tables)
    
    # tablenumber=[0,3,6,9,12]
    
    # for eachnumber in tablenumber:

        # thetable=tables[eachnumber].find('a').text.strip()
        # print(thetable)

        # theupdatetime=tables[eachnumber].find('div').text.strip()
        # print(theupdatetime)

        ##对于B1、C2策略，进行策略更新的跟踪
        # if eachnumber==9:
            # trs=tables[eachnumber].find_all('tr') #.find('tbody')
            # transactionitem="B1 超高频策略:" + trs[2].text.strip()
            ##print('transactionitem:' + transactionitem)
            ##print('gCurrentUpdateInfo_B2:' + gCurrentUpdateInfo_B2)
            
            # if gCurrentUpdateInfo_B2 != transactionitem:
                # print('!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
                # print('!!!!!!!!!!!!!!策略B1有更新!!!!!!!!!!!!')
                # print('!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
                # print(transactionitem) 
                #SendMail(transactionitem)
                # SendMessage(transactionitem)
                # gCurrentUpdateInfo_B2=transactionitem
                #print('gCurrentUpdateInfo_B2 new:' + gCurrentUpdateInfo_B2)
            # else:
                # print('')
            
    
        # if eachnumber==12:
            # trs=tables[eachnumber].find_all('tr') #.find('tbody')
            # transactionitem="C2 低频策略:" + trs[2].text.strip()
            ##print('transactionitem:' + transactionitem)
            ##print('gCurrentUpdateInfo_C1:' + gCurrentUpdateInfo_C1)
            
            # if gCurrentUpdateInfo_C1 != transactionitem:
                # print('!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
                # print('!!!!!!!!!!!!!!策略C2有更新!!!!!!!!!!!!')
                # print('!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
                # print(transactionitem) 
                ##SendMail(transactionitem)
                ##SendMessage(transactionitem)
                # gCurrentUpdateInfo_C1=transactionitem
    
        # thetable=tables[eachnumber].find_all('table')[1]
        # currentholding=thetable.find('td').text.strip()
        # print(currentholding)
        # print('#############################################################################')
        # print('\n')
	
	##print("current time:")
	##print(time_stamp.strftime('%Y.%m.%d-%H:%M:%S'))
    # print("当前时间：" + time_stamp.strftime('%Y.%m.%d-%H:%M:%S'))
	##system('cls')
	##print("当前时间：" + time_stamp.strftime('%Y.%m.%d-%H:%M:%S'))
    ##将输出栏清空
    ##sys.stdout.flush() 似乎无效
    # time.sleep(30)
    # os.system('cls')
	##system('cls')
	
    ##clear_output()
