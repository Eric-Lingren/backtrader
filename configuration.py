import backtrader as bt
import argparse

def parse_args():
    parser = argparse.ArgumentParser(
        description='Pandas test script')

    parser.add_argument('--noheaders', action='store_true', default=False,
                        required=False,
                        help='Do not use header rows')

    parser.add_argument('--noprint', action='store_true', default=False,
                        help='Print the dataframe')
    
    # parser.add_argument('--dataname', default='', required=False,
    #                     help='File Data to Load')

    # parser.add_argument('--timeframe', default='weekly', required=False,
    #                     choices=['daily', 'weekly', 'monhtly'],
    #                     help='Timeframe to resample to')

    # parser.add_argument('--compression', default=1, required=False, type=int,
    #                     help='Compress n bars into 1')

    return parser.parse_args()
