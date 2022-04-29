# import smtplib

# sender = 'aaronyinyong@hotmail.com'
# receivers = ['todo+urbd9px0uh72@mail.dida365.com']

# message = "This is a test e-mail message."

# try:
#    smtpObj = smtplib.SMTP('localhost')
#    smtpObj.sendmail(sender, receivers, message)         
#    print("Successfully sent email")
# # except SMTPException:
# except:
#    print("Error: unable to send email")

#coding=utf-8

from email.mime.text import MIMEText
from email.header import Header
from smtplib import SMTP_SSL


#qq邮箱smtp服务器
# host_server = 'smtp.qq.com'

host_server = 'smtp.office365.com'

#sender_qq为发件人的qq号码
# sender_qq = '105463201@qq.com'
sender_qq = 'aaronyinyong@hotmail.com'
#pwd为qq邮箱的授权码
# pwd = 'pmiglrpdmyzhbidb' ## xh**********bdc
pwd='aaronyinyong@hotmail.com'
#发件人的邮箱
sender_qq_mail = '105463201@qq.com'
#收件人邮箱
receiver ='todo+urbd9px0uh72@mail.dida365.com'
# receiver='aaronyinyong@hotmail.com'

#邮件的正文内容
mail_content = '#shf 晚上 滴答清单 from Python'
#邮件标题
mail_title = '邮件'

#ssl登录
smtp = SMTP_SSL(host_server)
#set_debuglevel()是用来调试的。参数值为1表示开启调试模式，参数值为0关闭调试模式
smtp.set_debuglevel(1)
smtp.ehlo(host_server)
smtp.login(sender_qq, pwd)

msg = MIMEText(mail_content, "plain", 'utf-8')
msg["Subject"] = Header(mail_title, 'utf-8')
msg["From"] = sender_qq_mail
msg["To"] = receiver
smtp.sendmail(sender_qq_mail, receiver, msg.as_string())
smtp.quit()