
from __future__ import (absolute_import, division, print_function,
                        unicode_literals)
import backtrader as bt
import datetime
from configuration import parse_args
from fetch_data import build_df
from strategies import *
from print_analysis import printTradeSummary, printSystemDrawdown, printSystemSharp


# data_filename = '/Volumes/External/test-data/test.h5'
# data_filename = '/Users/ericlingren/Desktop/week-1.h5'
# data_filename = '/Users/ericlingren/Documents/week-1.h5'
data_filename = '/Users/ericlingren/Documents/EURUSD-2019-1Min.csv'
cerebro = bt.Cerebro()





if __name__ == '__main__':
    # Congigure Pandas Arguments
    args = parse_args()
    
    # Add a strategy
    cerebro.addstrategy(RSITest)
    # cerebro.optstrategy(RSITest, loss_target=range(11,21))

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
    if len(df.columns) == 4:    
        data = bt.feeds.PandasData(dataname=df, open=0, high=1, low=2, close=3) 

    cerebro.adddata(data)

    cerebro.addobserver(bt.observers.DrawDown)

    cerebro.addanalyzer(bt.analyzers.TradeAnalyzer, _name="basic_stats")
    cerebro.addanalyzer(bt.analyzers.DrawDown, _name="draw_down")
    cerebro.addanalyzer(bt.analyzers.SharpeRatio, timeframe=bt.TimeFrame.Minutes, compression=5, factor=365, _name="sharpe")

    # cerebro.addobserver(bt.observers.Value)#

    # Set Account / Broker Data
    size = 10000
    cerebro.broker.setcash(1000.0)
    cerebro.broker.setcommission(commission=0.0000, leverage=50)
    cerebro.addsizer(bt.sizers.FixedSize, stake=size)

    print('\nStarting Portfolio Value: %.2f\n' % cerebro.broker.getvalue())

    # cerebro.run(maxcpus=3)
    strats = cerebro.run(maxcpus=3)
    strat = strats[0]

    print('\nFinal Portfolio Value: %.2f\n' % cerebro.broker.getvalue())

    printTradeSummary(strat.analyzers.basic_stats.get_analysis())
    printSystemDrawdown(strat.analyzers.draw_down.get_analysis())
    printSystemSharp(strat.analyzers.sharpe.get_analysis())

    # cerebro.plot(volume=False)

