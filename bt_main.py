
from __future__ import (absolute_import, division, print_function,
                        unicode_literals)
import backtrader as bt
import datetime
from configuration import parse_args
from fetch_data import build_df
from strategies import *
from print_analysis import printTradeSummary, printSystemDrawdown, printSystemSharp


#  Set Configs
pair = 'EURUSD'
year = '2015'
timeframe = '1Min'
display_chart = True
is_testing_optimization = False


data_root_path = '/Volumes/External/Trading/historical-data/forex/'
data_filename = data_root_path + pair + '/' + year + '/' + pair + '-' + year + '-' + timeframe + '.csv'  # CSV or H5
pos_size = 10000
cash = 1000

cerebro = bt.Cerebro()

if __name__ == '__main__':
    print(f'\n***** Running Backtest on {year} {pair} {timeframe} data *****')
    # Congigure Pandas Arguments
    args = parse_args()
    
    # Add a strategy
    if is_testing_optimization == False:
        cerebro.addstrategy(RSITest)
    else:
        cerebro.optstrategy(RSITest, profit_target=range(7,11))

    # Build Data Frame
    df = build_df(args, data_filename)

    # Load Data Frame into Backtrader
    if len(df.columns) == 2:    #  Formats data for tick datasets 
        data = bt.feeds.PandasData(dataname=df, high=0, low=1) 
    if len(df.columns) == 4:    #  Formats data for 1 min+ datasets 
        data = bt.feeds.PandasData(dataname=df, open=0, high=1, low=2, close=3) 
    cerebro.adddata(data)

    # Add Indicators to Image Plots
    cerebro.addobserver(bt.observers.DrawDown)

    # Add prebuilt data analyzers
    cerebro.addanalyzer(bt.analyzers.TradeAnalyzer, _name="basic_stats")
    cerebro.addanalyzer(bt.analyzers.DrawDown, _name="draw_down")
    cerebro.addanalyzer(bt.analyzers.SharpeRatio, timeframe=bt.TimeFrame.Minutes, compression=5, factor=365, _name="sharpe")

    # Set Account / Broker Data
    cerebro.broker.setcash(cash)
    cerebro.broker.setcommission(commission=0.0000, leverage=50)
    cerebro.addsizer(bt.sizers.FixedSize, stake=pos_size)

    # Run and Generate Reports
    print('\nStarting Portfolio Value: %.2f\n' % cerebro.broker.getvalue())

    if is_testing_optimization == False:
        strats = cerebro.run(maxcpus=3)
        strat = strats[0]
        printTradeSummary(strat.analyzers.basic_stats.get_analysis())
        printSystemDrawdown(strat.analyzers.draw_down.get_analysis())
        printSystemSharp(strat.analyzers.sharpe.get_analysis())
    else:
        cerebro.run(maxcpus=3)

    print('\nFinal Portfolio Value: %.2f\n' % cerebro.broker.getvalue())

    if display_chart == True:
        cerebro.plot(volume=False)

