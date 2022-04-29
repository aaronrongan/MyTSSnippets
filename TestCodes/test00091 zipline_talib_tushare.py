#测试zipline/talib/tushare是否安装好
#安装关键要点
# 通过conda install -c Quantopian zipline或ta-lib
#安装talib：通过Linux安装，参考量化学习笔记，很直接 sudo  make /make install 之类的
#或者Mac安装：先安装brew（会有xcode-select的报错），然后很快就装好
#或者Windows安装：conda update --all / conda install ta-lib -c QuantOpian

import zipline

import talib as ta

import tushare as ts


 