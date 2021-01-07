import os
import pandas
from .enums import Timeframe, Quote, Broker

cache = dict()

def load(timeframe:Timeframe, quote:Quote, broker:Broker=None):
    cache_key = (timeframe, quote, broker)

    if cache_key in cache:
        if cache[cache_key] is None:
            return None
        else:
            return cache[cache_key].copy()
    
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
            return dataframe

    cache[cache_key] = None
    return None
