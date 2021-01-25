import os
import pandas
from .enums import Timeframe, Quote, Broker, Col
from . import utils


cache = dict()


class Meta:
    def __init__(self, tf:Timeframe, qt:Quote, brk:Broker):
        self.timeframe = tf
        self.quote = qt
        self.broker = brk


def load(timeframe:Timeframe, quote:Quote, broker:Broker=None):
    meta = Meta(timeframe, quote, broker)
    cache_key = (timeframe, quote, broker)

    if cache_key in cache:
        if cache[cache_key] is None:
            return None, meta
        else:
            return cache[cache_key].copy(), meta
    
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
            
            _destructure_candles(dataframe, meta)
            cache[cache_key] = dataframe.copy()
            return dataframe, meta

    cache[cache_key] = None
    return None, meta


def _destructure_candles(df, df_meta:Meta):
    point_size = utils.point_size(df_meta.quote)
    wick_t, wick_b, body, rise, fall = [], [], [], [], []
    zipped_ohcl = zip(df[Col.OPEN]/point_size, df[Col.CLOSE]/point_size, df[Col.HIGH]/point_size, df[Col.LOW]/point_size)

    for op, cl, hi, lo in zipped_ohcl:
        sorted_prices = sorted([op, cl])
        wick_t += [hi-sorted_prices[-1]]
        wick_b += [sorted_prices[0]-lo]
        body += [cl - op]
        rise += [hi - op]
        fall += [op - lo]

    df[Col.WICK_T] = wick_t
    df[Col.WICK_B] = wick_b
    df[Col.RISE] = rise
    df[Col.FALL] = fall
    df[Col.BODY] = body