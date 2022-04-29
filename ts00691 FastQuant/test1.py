from fastquant import backtest, get_stock_data
jfc = get_stock_data("JFC", "2018-01-01", "2019-01-01",format="ohlcv")
backtest('smac', jfc, fast_period=15, slow_period=40)


# Starting Portfolio Value: 100000.00
# Final Portfolio Value: 1002272.90

# 作者：optMaster
# 链接：https://zhuanlan.zhihu.com/p/354714829
# 来源：知乎
# 著作权归作者所有。商业转载请联系作者获得授权，非商业转载请注明出处。