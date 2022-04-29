

# 微信消息接口及其它公共模块接口
import sys
sys.path.append('C:\\Users\\Aaron\\Documents\\MyMobileBooks_800_Reading\\MyTSSnippets\\CommonModules')

sys.path.append('C:\\Users\\Aaron\\Documents\\MyMobileBooks_800_Reading\\MyTSSnippets\\CommonModules\\WeChatAPIWrapper')



from jqdatasdk import *
import datetime

from abc import ABC, abstractmethod
import pandas as pd
import numpy as np

from DataFeeder import JQDataFeeder
import csv
import datetime
import os

from DataFeeder import *
from DataMaintain import DataMaintain
from WeChatAPIWrapper import WeChatAPIWrapper
from Util import *

import pandas as pd
import tushare as ts
import talib
from matplotlib import pyplot as plt
import datetime
import numpy as np
from dateutil.relativedelta import relativedelta

import smtplib  #用于发送邮件
from email.mime.text import MIMEText
from email.header import Header

from twilio.rest import Client
from requests.adapters import HTTPAdapter

import logging
from queue import Queue
import threading

# 为一些数据类提供更直接的表示，如Benchmark、Account、
from dataclasses import dataclass

# 用于寻找某些
import glob

import csv