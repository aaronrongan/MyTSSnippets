##PythonËØ?®Ä: Hotmail Âèë‰ø°
# -*- coding: utf-8 -*-
from email.mime.text import MIMEText
import smtplib

class Hotmail (object ):
    def __init__ (self ,account,password):
        self.account="%s@Hotmail.com" %account
        self.password=password

    def send (self ,to,title,content):
        print(self.account,self.password)
        server = smtplib.SMTPS('smtp.live.com' )
        ## server.set_debuglevel(1)
        server.docmd("EHLO server" )
        server.starttls()
        server.login(self.account,self.password)
        msg = MIMEText(content)
        msg['Content-Type' ]='text/plain; charset="utf-8"'
        msg['Subject' ] = title
        msg['From' ] = self.account
        msg['To' ] = to
        server.sendmail(self.account, to,msg.as_string())
        server.close()

class QQMail(object ):
    def __init__ (self ,account,password): 
        self.account="%s@qq.com" %account
        self.password=password

    def send (self ,to,title,content):
    # """
    # send('zsp007@Hotmail.com,zsp747@Hotmail.com")
    #     """
        print(self.account,self.password)
        server = smtplib.SMTP('smtp.qq.com' )
        server.set_debuglevel(1)
        ## server.docmd("EHLO server" )
        ## server.starttls()
        server.login(self.account,self.password)
        msg = MIMEText(content)
        msg['Content-Type' ]='text/plain; charset="utf-8"'
        msg['Subject' ] = title
        msg['From' ] = self.account
        msg['To' ] = to
        server.sendmail(self.account, to,msg.as_string())
        server.close()
 
if __name__=="__main__" : 
    Hotmail=Hotmail("aaronyinyong@hotmail.com","yinrong090114")
    Hotmail.send("105463201@qq.com","ÊµãËØïok" ,"content" )