# -*- coding: utf-8 -*-

import itchat

itchat.login()

# itchat.auto_login(hotReload=True)

# �������ѣ�search_friends("xxx"),����"xxx"Ϊ�����ǳƣ���ע��΢�ź�
userfinfo = itchat.search_friends("aaronyinyong3")


# userfinfo = itchat.search_friends("����Ⱥ�ܼ�014")   # "����Ⱥ�ܼ�014"Ϊ�����ǳ�

# print(userfinfo)����ȡuserinfo�е�UserName����
userid = userfinfo[0]["UserName"]   # ��ȡ�û�id

# ����΢�Žӿڷ�����Ϣ
itchat.send("hello dear", userid)  # ͨ���û�id������Ϣ
# ��
# itchat.send_msg(msg='hello dear', toUserName=userid)  # ���ʹ��ı���Ϣ