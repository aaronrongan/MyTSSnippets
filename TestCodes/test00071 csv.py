
#目的:如何读取一个CSV文件

# -*- coding: utf-8 -*-

import csv

codelist=[]

with open('StockList.csv',newline='') as csv_file:
# with open('StockList.csv',newline='', encoding = 'UTF-8') as csv_file:

    csv_reader = csv.DictReader(csv_file)
    for row in csv_reader:
        # print(row['code'],row['name'])
        codelist.append(row['code'])

 # print(codelist)
    # codelist=csv.reader(csv_file,delimiter=',')
    # for row in codelist:
    #         print(row.split(' '))
# csv_reader
# print(csv_reader.line_num)


