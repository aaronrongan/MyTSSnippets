# 目的
爬取果仁网站，找到需要的可以看到定义的页面

尝试破解，爬虫所有的公开策略，找到有定义的策略，发现新的因子
    

# 参考文献
- https://zhuanlan.zhihu.com/p/40178190 图形文字识别，训练库，彩色图形文字
- https://www.tensorflow.org/install/gpu tensorflow的使用
- https://pylessons.com/TensorFlow-CAPTCHA-solver-training/ TensorFlow教程
- https://docs.nvidia.com/cuda/cuda-installation-guide-microsoft-windows CUDA安装
- https://www.jianshu.com/p/f4e6ed72703a TensorFlow 安装GPU版本 
- https://www.cnblogs.com/shenh/p/9090586.html 异步编程
- https://blog.csdn.net/getcomputerstyle/article/details/103014896 python ahttp：简单、高效、异步requests请求模块
- https://zhuanlan.zhihu.com/p/34324225 python异步asyncio模块的使用 

# 主要相关网页
- https://guorn.com/user/home?page=created
- https://guorn.com/user/home?uid=332199&page=created
- https://guorn.com/stock/strategy?sid=9583.R.180706766085217
- https://guorn.com/user/profile?uid=4190 某个用户的账户情况，json格式
- https://github.com/duyet/bruteforce-database 密码库

# 代码
- Captcha_Pytorch_Application_1.ipynb https://colab.research.google.com/drive/1Jsz0JGCJnHWQT4DhV0cwBbrD1VYFIA5r#scrollTo=X3Uw3vnsZs6M
- ts00681.ipynb

# To Do List
-[ ] 列出所有的策略，看收益和回撤的最佳表现有哪些
-[ ] 将所有的密码图片都下载到本地，https://guorn.com/file/184266796033790.png，然后可以直接找到对应的文字，不用再破解
    不行，这是动态生成的
-[ ] 调用百度API进行图片识别，据说识别率比较高
    还是不行，图片文字歪斜扭转。可能需要用OpenCV等进行纠正
    收集 500 张图片来训练 Tesseract-ORC，识别率会有所提升，但识别率还是很低。如果想要做到识别率较高，那么需要使用 CNN (卷积神经网络)或者 RNN (循环神经网络)训练出自己的识别库.
    链接：https://www.jianshu.com/p/bc6774723003
-[ ] 爬取页面，抓出收益率大于30%以上的用户名，然后破解密码

# 记录

-这个登陆网址的解密
https://guorn.com/user/login
POST:
{
    account: "阿荣"
    cloud_login: 0
    code: null
    keep_login: "false"
    passwd: "arong1"    
}

如果不输入字符，返回错误
{"status": "need_captcha", "data": ""}
返回错误
{"status": "info", "data": "用户名或密码错误"}

-https://github.com/sirfz/tesserocr 图形码识别库

- 图形的生成网址
https://guorn.com/captcha/create 
POST: {"api":"/user/login"}

- 发送手机号解锁地址
https://guorn.com/user/findpass
POST：
{account: "17312656875"
captcha: "EZax"

- 策略导出网址：
https://guorn.com/stock/rule/save
{filters: [{industry: 0, id: "0.M.股票每日指标_市净率.0", op: "lt", type: "meas", val: "3"},…],…}
category: "stock"
current_tab: "back_test"
desc: ""
exclude_st: "1"
filter_suspend: true
filters: [{industry: 0, id: "0.M.股票每日指标_市净率.0", op: "lt", type: "meas", val: "3"},…]
name: "test_export"
ranks: [{id: "0.M.股票每日指标_动态市盈率.0", weight: 1, industry: 0, asc: true},…]
saveas: true
strategy_source: 0
tabs: {screen: {date: "2020/09/03", filter_suspend: true, original_vol: false, period: "5"},…}
target_shares: "阿荣"
timing: {,…}
visibility: 1

## 网页登录破解

### 暴力密码破解
- 密码组合 https://www.jianshu.com/p/9ce5093e0f24
0~9a~z 4位密码共160万个组合（为什么itertools.product算出来只有80万），一个测试需要1~1.5秒，共需要时间约1700小时
0~9a~z 5位密码共6000万个组合，需要时间6万小时
0~9a~z 6位密码共21亿个组合，需要时间220万小时

### TensorFlow、机器学习
https://zhuanlan.zhihu.com/p/26078299 使用深度学习来破解 captcha 验证码

https://github.com/ypwhs/captcha_break 计算机视觉：基于Python的深度学习
Tensorflow==1.15.3
Tensorflow_gpu=1.13.1

https://medium.com/@ageitgey/how-to-break-a-captcha-system-in-15-minutes-with-machine-learning-dbebb035a710

Deep Learning for Computer Vision with Python
(代码：https://github.com/TyroneLi/pyimagesearchcode )

https://blog.csdn.net/shebao3333/article/details/78808066 15分钟实战机器学习：验证码（CAPTCHA）识别

- TensorFlow/CUDA/Cudnn对应版本表
https://github.com/fo40225/tensorflow-windows-wheel 
1.13.1\py37\GPU\cuda101cudnn75sse2 	VS2017 15.9 	10.1.105_418.96/7.5.0.56 	x86_64 	Python 3.7/Compute 3.0
1.14.0\py37\GPU\cuda101cudnn76sse2  VS2019 16.1     10.1.168_425.25/7.6.0.64    x86_64  Python 3.7/Compute 3.0
1.15.0\py37\CPU+GPU\cuda101cudnn76sse2 	VS2019 16.3 	10.1.243_426.00/7.6.4.38 	x86_64 	Python 3.7/Compute 3.0
1.15.0\py37\CPU+GPU\cuda101cudnn76avx2 	VS2019 16.3 	10.1.243_426.00/7.6.4.38 	AVX2 	Python 3.7/Compute 3.0,3.5,5.0,5.2,6.1,7.0,7.5
1.15.0可以安装成功

- 看GPU是否存在命令
tf.test.is_gpu_available()

- Cudnn地址
https://developer.nvidia.com/rdp/cudnn-archive

- CUDA驱动
https://www.nvidia.com/download/index.aspx?lang=en-us
https://developer.nvidia.com/cuda-toolkit-archive
https://docs.nvidia.com/cuda/cuda-toolkit-release-notes/index.htm 

- PyTorch安装
在windows上，参考 https://pytorch.org/get-started/locally/
    pip install torch==1.6.0+cpu torchvision==0.7.0+cpu -f https://download.pytorch.org/whl/torch_stable.html --user（增加用户安装权限）
https://pytorch.org/get-started/previous-versions/ 
https://zhuanlan.zhihu.com/p/106944429 
安装命令：
pip install torch==1.5.1+cu101 torchvision==0.6.1+cu101 -f https://download.pytorch.org/whl/torch_stable.html
也可以将torch==1.5.1+cu101事先下载
以上安装成功。但是显卡性能不够，卡住了

重新编译适合3.0计算能力GPU的PyTorch
https://github.com/pytorch/pytorch#from-source 

Windows10 安装 Ubuntu
https://www.jianshu.com/p/8a62c020a553
https://docs.microsoft.com/zh-cn/windows/wsl/install-win10 

-  错误提示：with Cuda compute capability 3.0. The minimum required Cuda capability is 3.5.


- YouTube Captcha相关主题

- 知乎 “绕开网页登录”搜索
如换一个手机发送号

## git最简单安装
- https://git-scm.com/download/win windows界面git安装


## 具体流程
1. 登录网页
data = {"account":"13651829783","passwd":"aaronguorn"}
session = requests.Session()
response = session.post('https://guorn.com/user/login',data=json.dumps(data))

注意要用session的概念，来保存cookie

2. 搜索不同的ID，抓取公开的策略链接，包括名称、收益率、回撤率
realurl='https://guorn.com/user/strategy?uid=332199'
rec = requests.get(url=realurl)
if rec.status_code == 200:
    j = json.loads(rec.text) #解析之后的类型为字典类型
    results = j.get('data')#
    for i in results:

        print(i['name'],';',i['id'],';',i['annual_return'],';',i['max_withdraw'])

注意：实际显示的网页地址和真实的json格式不是同一个地址

3. 搜索策略对应的定义
url='https://guorn.com/stock/rule/definition?id=332199.R.89230182441435' #&sample=1&_=1599007602280
r = session.get(url)
- 重点项
name
ranks
Filters

## 有定义的策略
- https://guorn.com/user/home?uid=332199&page=created
- 自己的 https://guorn.com/user/home?page=created 


## 网页地址
        https://guorn.com/user/home?uid=9583&page=created
        然后找到 https://guorn.com/stock/strategy?sid=9583.R.180706766085217
            查看该网页有没有查看定义，如果有，列出导出到csv文件
        然后到https://guorn.com/stock?sid=332199.R.89230182441435&exec=1&category=stock#
            该网页导出策略总结
            设置权限的网页只有收藏，比较网页的不同
            
    uid和昵称的对应表，登录需要    
    大致用户在1~19000。但为什么自己的为402748？持有封基332199

## 网页流程
- 点击 https://guorn.com/user/home?uid=332199&page=created

- 实际有效列出所有策略的是
    https://guorn.com/user/strategy?uid=332199&_=1598782972909 #后面这个_=可能是时间

- 对应“查看定义”的为：
https://guorn.com/stock?sid=332199.R.89230182441435&exec=1&category=stock

- 对应'策略定义总结’的url：
https://guorn.com/stock/hotpool/all?category=stock&_=1598873666246 

- 自己的策略清单。和strategy页面如何区分？
https://guorn.com/stock/rule/all?_=1598874034795

- 自定的股票池清单
https://guorn.com/stock/pool/all?category=stock&_=1598918252495

- 系统股票池清单
https://guorn.com/stock/hotpool/all?category=stock&_=1598918252493

- 规则定义网址！！这个网址就是关键，如果没有认证，就会弹出没有权限
https://guorn.com/stock/rule/definition?id=332199.R.89230182441435&sample=1&_=1598874034798 （后面的sample/_=可以不用）

- 股票页面的基础数据
https://guorn.com/stock/meta?category=stock

- 回测结果数据 ！！！ 这里就是回测调仓的数据
https://guorn.com/stock/backtest?sid=332199.R.89230182441435&_=1598918252498 （有定义可以返回）
https://guorn.com/stock/backtest?sid=9583.R.180706766085217&_=1598918252498 （没有数据返回）

- 返回用户配置文件
https://guorn.com/user/profile?_=1598919405737
其中的request cookie为：
token="2|1:0|10:1598873971|5:token|76:ZWEyOGU5ZTkyZTRiYjIxNDMwNGE2ODA3YmI1YjA3YmY3MjFlODdjOGEzMGNiMDY3Y2Y0NjYyMzc=|d7cfb1c2f8cc9d8726bfb1ce01d4d09b53327085f7d59ad874ca3c0e31931369"; tempStrategyOwner=13651829783; _gat=1; user="2|1:0|10:1598873971|4:user|8:NDAyNzQ4|4d0707c6debaa48931a56a1d444e656a9e82a6f9f06f4e26416b26a816b2aadb"; _gid=GA1.2.1196045778.1598766960; sv="2|1:0|10:1598872818|2:sv|4:MTE=|cc8d508cca905f14514f31515b529bb7d1d2bd7159d94e49a4b18dffb307a88b"; Hm_lvt_40ee94ccee2cf1051316f73e3fbcf8ac=1598766960,1598769156,1598782694,1598831663; _ga=GA1.2.1926308829.1598675953; captcha="2|1:0|10:1598873955|7:captcha|60:YzFlZWJlNzAwMjhhNTc3MGQ5ZDk3MTJlYjRhYWViMzU6L3VzZXIvbG9naW4=|7203a3e6083917791444e7127dd3b8a0d9f55d696462e6acea87160b1d055112"; account="2|1:0|10:1598873971|7:account|16:MTM2NTE4Mjk3ODM=|f8894cabb07478ff70fd9998f66c7098838a3d3d586d6ca4a239b7ee11c7ca76"; uname="2|1:0|10:1598873971|5:uname|16:IOamleahieeIuA==|05817116e879820b4aef804fcb336b0ad3f49345722891f1d4e5e93e0434dd34"; _xsrf=2|0f6c84d1|560498120eea3fddc8da464f0588cf50|1598831664; Hm_lpvt_40ee94ccee2cf1051316f73e3fbcf8ac=1598873973

## BeautifulSoup转为Json格式
realurl='https://guorn.com/user/strategy?uid=332199'


# 日志

-200920
比较郁闷，竟然被果仁查到了自己的手机，只好停止。。。
花费3周总算搞定之时，却发现被人发现。。。看来违法的事不要做。。。
搞的兴趣全无。不过还是学到了不少知识

后续任务
    优化异步编程，搞清楚一些函数的区别，如await/asyncio.as_completed/run_until_complete
    tqdm进度条如何运用？
    多线程是否有助提高速度？
    尝试3台电脑同时破解？将密码分3组。如一个用colab，一个用vs，分成不同的IP来求解
    记录破解过程，已经测试了哪些数据
    搞清异步的机理为什么是生成器generator
    coroutine/future的内涵和应用

-200919
学会异步，可以实现异步抓取登录破解，单个网页抓取平均时间从2~4秒降到0.1秒，非常明显
下一步计划：
    多线程是否可以提高？
    
-200918
学会协程asyncio/，以及进程、线程的区别

-200917
成功编写出果仁解码程序。问题在于6位的时间太长。也许同步可以解决，登录、下载和分析图片需要时间
用线程池来解决

-200916
成功靠Colab计算出ctc.pth，并且成功计算出果仁图片，果仁的图片就是ImageCaptcha的库，4位，160X40大小

-200914
又尝试了Windows的PyTorch编译，搞了一天，终于成功。
却又郁闷的发现ZBook 15 G1的 GPU 2G根本不够用。
准备放弃时，上网发现了CoLab，可以在云端运行PyTorch程序，成功率很高

-200912
周五试图在本地编译Linux的Torch，终于成功。
但是发现无法用Linux的CUDA，很郁闷的试了周六周日，还是没有解决。
虚拟机上的这个显卡驱动一直有问题

-200908~11
安装CUDA、CUDNN，发现GPU无法运行，郁闷的发现因为K2100M的计算力只有3，而TensorFlow和PyTorch至少要3.5以上计算力的显卡

-200904~08
尝试用tensorflow来解决captcha解密。但是最后受困于tensorflow/CUDA/CuDNN的安装，没有进一步进展
继续尝试用PyTorch解决

-200902
成功实现定义抓取。总结流程见‘具体流程’

-200901
找到策略定义网址，理论上可以实现遍历：按ID顺序依次搜索策略，然后将策略的定义列出，这样可以遍历所有用户的策略定义
存在问题：有权限的无法访问，就需要破解用户密码


-200831
开始编写代码，找到策略相关网址



# 问题及解决
1. Json解析错误
definitionurl='https://guorn.com/stock/rule/definition?id=332199.R.89230182441435&sample=1'
response_json = requests.get(definitionurl).json()
JSONDecodeError: Expecting value: line 1 column 1 (char 0)
原因在于没有登录，返回的不是json，而是HTML格式
需要登录
https://guorn.com/user/login
https://guorn.com/user/login?next=/stock/rule/definition?id%=332199.R.89230182441435&sample=1

关键在于直接用data不能用,而要用json.dumps(data)
data = {"account":"13651829783","passwd":"aaronguorn"}
错误：response = requests.post('https://guorn.com/user/login',data=data)
正确：response = requests.post('https://guorn.com/user/login',data=json.dumps(data))

2. 如何找到uid对应的account名称？比如uid=4039，account=持有封基，这样就可以尝试破解密码？

3. - https://guorn.com/user/login 这个页面如何登录？如何破解
Request Body {"account":"13651829783","passwd":"aaronguorn","keep_login":"true","code":null,"cloud_login":0}
Response Body {"status": "ok", "data": {"username": " \u6995\u6849\u7238", "account": "13651829783", "uid": 402748}}
用session然后post方式，response = requests.post('https://guorn.com/user/login',data=json.dumps(data))
session = requests.Session()
- 

4. 使用tesserocr
Failed to init API, possibly an invalid tessdata
https://blog.csdn.net/moxiao1995071310/article/details/82630996
tessdata放到C:\Users\Aaron\AppData\Local\Programs\Python\Python37\tessdata

5. 验证码识别时导入captcha.image出错
自己的文件名写成了captcha

6. tensorflow问题
DLL load failed: The specified module could not be found.
I solved it today downloading and installing visual studio 2015-2019 x86 and x64 from here:
https://support.microsoft.com/en-us/help/2977003/the-latest-supported-visual-c-downloads
Other solution is downgrading tensorflow to 2.0:
pip install tensorflow==2.0
https://www.tensorflow.org/install/gpu 

7. 重新编译PyTorch
https://github.com/pytorch/pytorch#from-source
https://zhuanlan.zhihu.com/p/106977910 

8. 用asyncio，在notebook报错This event loop is already running
import nest_asyncio
nest_asyncio.apply()
