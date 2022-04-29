## %%
# zipline --start 2017-1-2 --end 2017-12-29 --capital-base 250 --bundle eu_stocks -o buy_and_hold.pkl --trading-calendar XAMS

import pandas as pd
import matplotlib.pyplot as plt
# imports
from zipline import run_algorithm
from zipline.api import order, symbol, record, set_benchmark

# %matplotlib inline

# parameters

selected_stock = 'ABN'

n_stocks_to_buy = 10



def initialize(context):

    set_benchmark(symbol('AEX'))

    context.asset = symbol('ABN')

    context.has_ordered = False  



def handle_data(context, data):

    # record price for further inspection

    record(price=data.current(symbol(selected_stock), 'price'))

    print('handle_data')

    # trading logic

    if not context.has_ordered:

        # placing order, negative number for sale/short

        order(symbol(selected_stock), n_stocks_to_buy)

        # setting up a flag for holding a position

        context.has_ordered = True


def analyze(context, perf):
    fig = plt.figure()
    ax1 = fig.add_subplot(111)
    perf.portfolio_value.plot(ax=ax1)
    ax1.set_ylabel('portfolio $ value')
    plt.legend(loc=0)
    plt.show()    




if __name__ == '__main__':
    capital_base = 200000
    start = pd.to_datetime('2015-01-01').tz_localize('US/Eastern')
    
    print(start)

    end = pd.to_datetime('2018-02-01').tz_localize('US/Eastern')
    print(end)

    # result = run_algorithm(start=start, end=end, initialize=initialize,
    #                        capital_base=capital_base, handle_data=handle_data,
    #                        bundle='quantopian-quandl', analyze=analyze)
    result = run_algorithm(start=start, end=end, initialize=initialize,
                           capital_base=capital_base, handle_data=handle_data,
                           bundle='eu_stocks', analyze=analyze)