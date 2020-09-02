
from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import backtrader as bt
import datetime
from configuration import parse_args
from fetch_data import build_df
from strategies import *


# data_filename = '/Volumes/External/test-data/test.h5'
data_filename = '/Users/ericlingren/Desktop/test.h5'
cerebro = bt.Cerebro()


if __name__ == '__main__':
    # Congigure Pandas Arguments
    args = parse_args()
    
    # Add a strategy
    cerebro.addstrategy(PrintPrices)

    # Build Data Frame
    df = build_df(args, data_filename)

    # Load Data Frame into Backtrader
    data = bt.feeds.PandasData(dataname=df, high=0, low=1)
    cerebro.adddata(data)

    # Set Account Value
    cerebro.broker.setcash(100000.0)

    print('Starting Portfolio Value: %.2f' % cerebro.broker.getvalue())

    cerebro.run()

    print('Final Portfolio Value: %.2f' % cerebro.broker.getvalue())

