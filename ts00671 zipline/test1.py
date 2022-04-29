from zipline.api import order, record, symbol
from zipline.finance import commission, slippage
from zipline import run_algorithm
import pandas as pd

import matplotlib.pyplot as plt

def initialize(context):
    context.asset = symbol('AAPL')
    context.set_commission(commission.PerShare(cost=.0075, min_trade_cost=1.0))
    context.set_slippage(slippage.VolumeShareSlippage())


def handle_data(context, data):
    order(context.asset, 10)
    record(AAPL=data.current(context.asset, 'price'))

def analyze(context=None, results=None):
    # import matplotlib.pyplot as plt
    # Plot the portfolio and asset data.
    ax1 = plt.subplot(211)
    results.portfolio_value.plot(ax=ax1)
    ax1.set_ylabel('Portfolio value (USD)')
    ax2 = plt.subplot(212, sharex=ax1)
    results.AAPL.plot(ax=ax2)
    ax2.set_ylabel('AAPL price (USD)')

    # Show the plot.
    plt.gcf().set_size_inches(18, 8)
    plt.show()


def _test_args():
    """Extra arguments to use when zipline's automated tests run this example.
    """
    import pandas as pd

    return {
        'start': pd.Timestamp('2014-01-01', tz='utc'),
        'end': pd.Timestamp('2016-11-01', tz='utc'),
    }


if __name__ == '__main__':
    capital_base = 200000
    start = pd.to_datetime('2015-01-01').tz_localize('US/Eastern')
    
    print(start)

    end = pd.to_datetime('2018-02-01').tz_localize('US/Eastern')
    print(end)

    result = run_algorithm(start=start, end=end, initialize=initialize,
                           capital_base=capital_base, handle_data=handle_data,
                           bundle='quantopian-quandl', analyze=analyze)