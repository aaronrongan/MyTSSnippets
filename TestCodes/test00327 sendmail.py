# -*- coding: utf-8 -*-

import smtplib
from email.mime.text import MIMEText
from email.header import Header

from_addr='aaronyinyong@hotmail.com'   #发送账号
# to_addrs='todo+Surbd9px0uh72@mail.dida365.com'   #接收账号
to_addrs='todo@mail.dida365.com'
# to_addrs='aaronyinyong@hotmail.com'   #接收账号
# qqCode='pmiglrpdmyzhbidb'   #授权码
qqCode='yinrong090114'
smtp_server='smtp.office365.com'
smtp_port=587


#配置服务
# stmp=smtplib.SMTP_SSL(smtp_server,smtp_port)
smtp=smtplib.SMTP(smtp_server,smtp_port)

smtp.ehlo()
smtp.starttls()

smtp.login('aaronyinyong@hotmail.com','yinrong090114')


message = MIMEText('Task3', 'plain', 'utf-8')   
message['From'] = Header("Python Test", 'utf-8')   
# message['To'] = Header("todo+Surbd9px0uh72@mail.dida365.com", 'utf-8')   
message['To'] = 'todo+urbd9px0uh72@mail.dida365.com' # 'todo@mail.dida365.com'
subject = 'Python SMTP test'
message['Subject'] = Header('Task3', 'utf-8') 

try:
    smtp.sendmail('aaronyinyong@hotmail.com', 'todo@mail.dida365.com', message.as_string())
    print ('send successful')
except Exception as e:
    print ('send error' + str(e))
