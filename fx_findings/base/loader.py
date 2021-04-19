import os
import pandas
import numpy as np
from .enums import Timeframe, Quote, Broker, Col
from . import utils


cache = dict()


class Meta:
    def __init__(self, tf:Timeframe, qt:Quote, brk:Broker):
        self.timeframe = tf
        self.quote = qt
        self.broker = brk


def load_price_dataset(timeframe:Timeframe, quote:Quote, broker:Broker=None):
    meta = Meta(timeframe, quote, broker)
    cache_key = (timeframe, quote, broker)

    if cache_key in cache:
        if cache[cache_key] is None:
            return None, meta
        else:
            return cache[cache_key].copy(), meta
    
    if timeframe == Timeframe.D2:
        grouping = 2
        timeframe = Timeframe.D1
    elif timeframe == Timeframe.D3:
        grouping = 3
        timeframe = Timeframe.D1
    else:
        grouping = None
    
    directory = f'data/{timeframe}/{quote}'

    if not broker is None:
        directory += '/' + broker

    for filename in os.listdir(directory):
        if filename.endswith(".csv"): 
            filepath = os.path.join(directory, filename)
            if timeframe == Timeframe.D1:
                dataframe = pandas.read_csv(filepath, sep='\t', parse_dates={'<DATETIME>':[0]}, infer_datetime_format=True)
            else:
                dataframe = pandas.read_csv(filepath, sep='\t', parse_dates={'<DATETIME>':[0,1]}, infer_datetime_format=True)
            
            if not grouping is None:
                print(dataframe.shape)
                _group_up_candles(dataframe, meta, grouping)
                print(dataframe.shape)  
            _destructure_candles(dataframe, meta)

            cache[cache_key] = dataframe.copy()
            return dataframe, meta

    cache[cache_key] = None
    return None, meta

def _group_up_candles(df, df_meta:Meta, grouping:int):
    num_row = df.shape[0]
    remainder = num_row % grouping

    if remainder != 0:
        df.drop(np.arange(num_row-remainder,num_row), inplace=True)
        num_row = df.shape[0]

    if num_row == 0:
        return

    print(df[:grouping*2])

    for i in range(0, num_row, grouping):
        o = df.iloc[i][Col.OPEN]
        c = df.iloc[i+grouping-1][Col.CLOSE]
        h = max(df.iloc[i:i+grouping][Col.HIGH])
        l = min(df.iloc[i:i+grouping][Col.LOW])
        v = sum(df.iloc[i:i+grouping][Col.VOL])
        s = max(df.iloc[i:i+grouping][Col.SPREAD])

        next_i = i//grouping
        df.iloc[next_i, df.columns.get_loc(Col.DATETIME)] = df.iloc[i][Col.DATETIME]
        df.iloc[next_i, df.columns.get_loc(Col.OPEN)] = o
        df.iloc[next_i, df.columns.get_loc(Col.CLOSE)] = c
        df.iloc[next_i, df.columns.get_loc(Col.HIGH)] = h
        df.iloc[next_i, df.columns.get_loc(Col.LOW)] = l
        df.iloc[next_i, df.columns.get_loc(Col.VOL)] = v
        df.iloc[next_i, df.columns.get_loc(Col.SPREAD)] = s
    
    print(df[:grouping*2])
    
    df.drop(np.arange(num_row//grouping, num_row), inplace=True)

def _destructure_candles(df, df_meta:Meta):
    point_size = utils.market.point_size(df_meta.quote)
    wick_t, wick_b, body, rise, fall, height = [], [], [], [], [], []
    zipped_ohcl = zip(df[Col.OPEN]/point_size, df[Col.CLOSE]/point_size, df[Col.HIGH]/point_size, df[Col.LOW]/point_size)

    for op, cl, hi, lo in zipped_ohcl:
        sorted_prices = sorted([op, cl])
        wick_t += [hi-sorted_prices[-1]]
        wick_b += [sorted_prices[0]-lo]
        body += [cl - op]
        rise += [hi - op]
        fall += [op - lo]
        height += [hi-lo]

    df[Col.WICK_T] = wick_t
    df[Col.WICK_B] = wick_b
    df[Col.RISE] = rise
    df[Col.FALL] = fall
    df[Col.BODY] = body
    df[Col.HEIGHT] = height