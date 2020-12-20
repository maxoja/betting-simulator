import os
import pandas
from enums import Timeframe, Quote, Broker

def load(timeframe:Timeframe, quote:Quote, broker:Broker=None):
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
            return dataframe

    return None
