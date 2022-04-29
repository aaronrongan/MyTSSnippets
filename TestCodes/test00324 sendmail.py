# -*- coding: utf-8 -*-

import smtplib
from email.mime.text import MIMEText
from email.header import Header

from_addr='105463201@qq.com'   #�?��发送账�?
to_addrs='todo+Surbd9px0uh72@mail.dida365.com'   #接收�?��账号
# to_addrs='aaronyinyong@hotmail.com'   #接收�?��账号
# qqCode='pmiglrpdmyzhbidb'   #授权码（这个要填�?��获取到的�?
qqCode='zzupdnrgvgxrbgge'
smtp_server='smtp.qq.com'
smtp_port=465#固定�?��


#配置服务�?
stmp=smtplib.SMTP_SSL(smtp_server,smtp_port)
stmp.login(from_addr,qqCode)

#组�?发送内�?
message = MIMEText('我是发送的内�?', 'plain', 'utf-8')   #发送的内�?
message['From'] = Header("Python�?��预�?系统", 'utf-8')   #发件�?
message['To'] = Header("管理�?", 'utf-8')   #收件�?
subject = 'Python SMTP �?��测试'
message['Subject'] = Header(subject, 'utf-8')  #�?��标�?

try:
    stmp.sendmail(from_addr, to_addrs, message.as_string())
except Exception as e:
    print ('�?��发送失�?--' + str(e))
print ('�?��发送成�?')