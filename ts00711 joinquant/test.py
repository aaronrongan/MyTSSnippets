from jqdatasdk import *
# 导入函数库
from jqdatasdk import get_factor_values


auth('18136078552','078552')

# 获取因子Skewness60(个股收益的60日偏度)从 2017-01-01 至 2017-03-04 的因子值
#factor_data = get_factor_values(securities=['000001.XSHE'], factors=['Skewness60','DEGM','quick_ratio'], start_date='2017-01-01', end_date='2017-03-04')
# 查看因子值
#print(factor_data['Skewness60'][:5])

#df = get_all_factors()
#print(df) 

# 导入 Alpha101 库
from jqdatasdk.alpha101 import *

# 查询函数说明
help(alpha_001)

a = alpha_001('2019-11-19','000300.XSHG')

# 查看前5行的因子值
print(a.head())


# 定义股票池列表
security_list1 = '000001.XSHE'
security_list2 = ['000001.XSHE','000002.XSHE','601211.XSHG','603177.XSHG']

# 计算并输出 security_list1 的 ACCER 值
ACCER1 = ACCER(security_list1, check_date='2017-01-04', N = 8)
print(ACCER1[security_list1])

# 输出 security_list2 的 ACCER 值
ACCER2 = ACCER(security_list2, check_date='2017-01-04', N = 8)
for stock in security_list2:
    print(ACCER2[stock])