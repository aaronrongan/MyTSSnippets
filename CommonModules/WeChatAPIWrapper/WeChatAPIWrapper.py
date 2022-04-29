import sys
sys.path.append('C:\\Users\\Aaron\\Documents\\MyMobileBooks_800_Reading\\MyTSSnippets\\CommonModules')
sys.path.append('C:\\Users\\Aaron\\Documents\\MyMobileBooks_800_Reading\\MyTSSnippets\\CommonModules\\WeChatAPIWrapper')

# WechatPCAPI的使用
from WechatPCAPI import WechatPCAPI
import time
import logging
from queue import Queue
import threading

class WeChatAPIWrapper():

    # self.wx_inst=''

    def __init__(self):
        
        logging.basicConfig(level=logging.INFO)
        self.queue_recved_message = Queue()

    def Start(self):
        self.wx_inst = WechatPCAPI(on_message=self.on_message, log=logging)
        # print('wx_inst')
        # wx_inst.start_wechat(block=False)
        self.wx_inst.start_wechat(block=True)
        print('wx_inst.start_wechat##########')
        while not self.wx_inst.get_myself():
            time.sleep(5)
            print('while not...')
        
        print('登陆成功')
        print(self.wx_inst.get_myself())

        threading.Thread(target=self.thread_handle_message, args=(self.wx_inst,)).start()
        # time.sleep(10)

    def on_message(self,message):
        self.queue_recved_message.put(message)
        # 消息处理示例 仅供参考


    def thread_handle_message(self, wx_inst):

        while True:
            message = self.queue_recved_message.get()
            # print(message)
            # if 'msg' in message.get('type'):
            #     # 这里是判断收到的是消息 不是别的响应
            #     msg_content = message.get('data', {}).get('msg', '')
            #     send_or_recv = message.get('data', {}).get('send_or_recv', '')
            #     if send_or_recv[0] == '0':
            #         # 0是收到的消息 1是发出的 对于1不要再回复了 不然会无限循环回复
            #         wx_inst.send_text('filehelper', '收到消息:{}'.format(msg_content))

    # @staticmethod
    # 和SendMessage同一个意思
    # 文件管理助手 'filehelper'
    def SendWeChatMessage(self, Message,UserID='aaronyinyong'):
        time.sleep(2)
        self.wx_inst.send_text(to_user=UserID, msg=Message)
    
    def SendMessage(self, Message,UserID='aaronyinyong'):
        time.sleep(2)
        # self.wx_inst.send_text(to_user=UserID, UserID=UserID, msg=Message)
        self.wx_inst.send_text(to_user=UserID, msg=Message)
        

# wechat=WeChatAPIWrapper()
# wechat.Start()
# wechat.SendMessage('Hello WeChat')
