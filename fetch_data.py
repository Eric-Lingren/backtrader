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
                        key='/FX_test-2020-1_tick', 
                        skiprows=skiprows,
                        header=header,
                        parse_dates=True,
                        index_col=0)

    # Configure Data Frame
    df.columns = ['ASKP', 'BIDP']
    df.index = pd.to_datetime(df.index, format='%Y-%m-%d %H:%M:%S:%f')

    print(df.head())
    print("\nData loaded in %s Seconds" % (time.time() - start_time))

    return df