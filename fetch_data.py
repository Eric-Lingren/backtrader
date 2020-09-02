import os
import sys
import pandas as pd
import time


def build_df(args, filename):
    start_time = time.time()
    print('Loading Data File...')

    # Configure Pandas Headers
    skiprows = 1 if args.noheaders else 0
    header = None if args.noheaders else 0

    # Build Data Frame
    df = pd.read_hdf(   filename, 
                        # key='/FX_test-2020-1_tick', 
                        skiprows=skiprows,
                        header=header,
                        parse_dates=True,
                        index_col=0)

    #  Assigns column names and formats timestamps for tick datasets 
    if len(df.columns) == 2:
        df.columns = ['ASKP', 'BIDP']
        df.index = pd.to_datetime(df.index, format='%Y-%m-%d %H:%M:%S:%f')

    #  Assigns column names and formats timestamps for 1 min+ datasets 
    if len(df.columns) == 5:    
        df.columns = ['OPEN', 'HIGH', 'LOW', "CLOSE", "VOLUME"]
        df.index = pd.to_datetime(df.index, format='%d.%m.%Y %H:%M:%S.%f')

    # df.index = pd.to_datetime(df.index, format='%Y-%m-%d %H:%M:%S.%f') # For Tick Data
    # df.index = pd.to_datetime(df.index, format='%d.%m.%Y %H:%M:%S.%f') # For Downlaoded CSV Minute Format

    # print(df.head())
    print("\nData loaded in %s Seconds" % (time.time() - start_time))

    return df