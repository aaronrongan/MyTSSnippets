# -*- coding: utf-8 -*-


#pip install wxpy

from __future__ import unicode_literals
from threading import Timer
from wxpy import *
import requests

#������
bot = Bot()

def get_news():
    url = "http://open.cicba.com/dsapi/"
    r = requests.get(url)
    content = r.json()['content']
    note = r.json()['note']
    return content,note

def send_news(str):
    try:
        #contents = [2,2,3]
        #�����б�  ��ע��ʾ
        #print(bot.friends())
        print(bot.friends().search(u'aaronyinyong3'))
        # ΢���ǳƣ������˺�
        #my_friend = bot.friends().search(u'Ī')[0]
        #����
        #my_friend.send(contents[0])
        #����ͼƬ
        #my_friend.send_image("C:\\Users\\Administrator.000\\Desktop\\intiloading.png")
        # ������Ƶ
        #my_friend.send_video('my_video.mov')
        # �����ļ�
        #my_friend.send_file('my_file.zip')
        # �Զ�̬�ķ�ʽ����ͼƬ   ûɶ��
        # my_friend.send('@img@C:\\Users\\Administrator.000\\Desktop\\intiloading.png')
        # t = Timer(86400,send_news("kaishi"))
        # t.start()

        print(bot.groups)#<bound method Bot.groups of <Bot: ��깥��ʨ>>
        #bot�����ﺬ��chats��friends��groups��mps�ȷ������ֱ���Ի�ȡ��ǰ�����˵�������󡢺��ѡ�Ⱥ�ġ����ںŵ���Ϣ
        all_group = bot.groups()
        print("type all:",type(all_group))
        print(all_group)  #[<Group: �һ��������������ڲ�����Ⱥ>, <Group: �������ܿƼ�������ͨ>]
        for i in all_group:
            Group = str(i)
            group = Group.replace("<Group: ","").replace(">","")
            #send=bot.groups().search(group)[0].send_image("1.jpg")
            print(Group)
            print(group)
            # print(send)

        #���ܷ����Լ��ᱨ��
        # my = bot.friends().search(u'��깥��ʨ')[0]
        # my.send("����")
    except :
        my = bot.friends().search(u'aaronyinyong3')[0]
        my.send("error to send")

if __name__ == '__main__':
    # str = input("����q�˳�")
    # if str == "q":
    #     exit(0)
    # else:
    send_news(str)

    #sys.exit()
# ��������������������������������
# ��Ȩ����������ΪCSDN������onj123����ԭ�����£���ѭ CC 4.0 BY-SA ��ȨЭ�飬ת���븽��ԭ�ĳ������Ӽ���������
# ԭ�����ӣ�https://blog.csdn.net/onj123/article/details/81747745