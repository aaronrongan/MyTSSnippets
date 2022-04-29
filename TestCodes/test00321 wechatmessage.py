# -*- coding: utf-8 -*-

import itchat

itchat.login()

# itchat.auto_login(hotReload=True)

# 搜索好友，search_friends("xxx"),其中"xxx"为好友昵称，备注或微信号
userfinfo = itchat.search_friends("aaronyinyong3")


# userfinfo = itchat.search_friends("智能群管家014")   # "智能群管家014"为好友昵称

# print(userfinfo)，获取userinfo中的UserName参数
userid = userfinfo[0]["UserName"]   # 获取用户id

# 调用微信接口发送消息
itchat.send("hello dear", userid)  # 通过用户id发送信息
# 或
# itchat.send_msg(msg='hello dear', toUserName=userid)  # 发送纯文本信息