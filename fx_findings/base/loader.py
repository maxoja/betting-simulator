import os
import pandas
from .enums import Timeframe, Quote, Broker

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
            
            cache[cache_key] = dataframe.copy()
            return dataframe, meta

    cache[cache_key] = None
    return None, meta