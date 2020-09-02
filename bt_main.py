
from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import backtrader as bt
import datetime
from configuration import parse_args
from fetch_data import build_df
from strategies import *


# data_filename = '/Volumes/External/test-data/test.h5'
data_filename = '/Users/ericlingren/Desktop/week-1.h5'
# data_filename = '/Users/ericlingren/Desktop/EURUSD-1-min.h5'
cerebro = bt.Cerebro()


if __name__ == '__main__':
    # Congigure Pandas Arguments
    args = parse_args()
    
    # Add a strategy
    cerebro.addstrategy(PrintTickPrices)

    # Build Data Frame
    df = build_df(args, data_filename)

    # tframes = dict(
    #     daily=bt.TimeFrame.Days,
    #     weekly=bt.TimeFrame.Weeks,
    #     monthly=bt.TimeFrame.Months)

    # Load Data Frame into Backtrader

        #  Formats data for tick datasets 
    if len(df.columns) == 2: 
        data = bt.feeds.PandasData(dataname=df, high=0, low=1) 
    
        #  Formats data for 1 min+ datasets 
    if len(df.columns) == 5:    
        data = bt.feeds.PandasData(dataname=df, open=0, high=1, low=2, close=3) 

    # cerebro.resampledata(data, timeframe=bt.TimeFrame.Minutes, compression=2)
    cerebro.adddata(data)

    # Set Account Value
    cerebro.broker.setcash(100000.0)

    print('Starting Portfolio Value: %.2f' % cerebro.broker.getvalue())

    cerebro.run()

    print('Final Portfolio Value: %.2f' % cerebro.broker.getvalue())

