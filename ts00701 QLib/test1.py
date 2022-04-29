import qlib
from qlib.data import D
#qlib.init(provider_uri='~/.qlib/qlib_data/cn_data')
qlib.init(provider_uri='C:/Users/aaron/Documents/qlib/qlib_data/cn_data')
instruments = D.instruments(market='csi300')
D.list_instruments(instruments=instruments, start_time='2010-01-01', end_time='2017-12-31', as_list=True)[:20]