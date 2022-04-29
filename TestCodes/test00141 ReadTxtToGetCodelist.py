
# -*- coding: utf-8 -*-

#读取文本文件，得到第一列的代码

import re

f = open("StockList.txt",'r', encoding='UTF-8')

# s=f.read()
# s1 = re.split(' ', s) #利用正则函数进行分割
# for i in s1:
#     print(i)
i=0
codelist=[]
codelist.append(0)

while True:
    lines=f.readline()
    if not (lines or lines=='\n'):
        break
    else:
        s1 = re.split(' ', lines)
        codelist[i] = s1[0]
        i = i + 1
        codelist.append(1)

print(i)
print(codelist)
#bug: codelist会多出最后一个数