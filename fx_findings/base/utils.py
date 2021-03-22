import numpy as np
from .enums import Quote, Col, Timeframe, PosType


def slice_frame_from_back(df, size, shift_end=0, buffer=0):
    if shift_end < 0 or size+buffer+shift_end >= len(df):
        return None
        
    start = (-size-shift_end-buffer)
    end = len(df)-shift_end
    return df[start:end]


def slice_frame_from_front(df, size, shift_front=0, buffer=0):
    start = shift_front - buffer
    end = shift_front + size

    if start < 0 or end >= len(df):
        raise ValueError()

    return df[start:end]


def average_spread(df):
    series = df[Col.SPREAD]
    return sum(series)/len(series)


def point_size(quote:Quote):
    return __point_size_of[quote]


def pip_size(quote:Quote):
    return point_size(quote)*10


def annual_bars(timeframe:Timeframe):
    return __annual_bars_of[timeframe]

__point_size_of = {
    Quote.AUDCAD: 0.00001,
    Quote.AUDCHF: 0.00001,
    Quote.AUDJPY: 0.001,
    Quote.AUDNZD: 0.00001,
    Quote.AUDUSD: 0.00001,
    Quote.CADCHF: 0.00001,
    Quote.CADJPY: 0.001,
    Quote.CHFJPY: 0.001,
    Quote.EURAUD: 0.00001,
    Quote.EURCAD: 0.00001,
    Quote.EURCHF: 0.00001,
    Quote.EURGBP: 0.00001,
    Quote.EURJPY: 0.001,
    Quote.EURNZD: 0.00001,
    Quote.EURUSD: 0.00001,
    Quote.GBPAUD: 0.00001,
    Quote.GBPCAD: 0.00001,
    Quote.GBPCHF: 0.00001,
    Quote.GBPJPY: 0.001,
    Quote.GBPNZD: 0.00001,
    Quote.GBPUSD: 0.00001,
    Quote.NZDCAD: 0.00001,
    Quote.NZDCHF: 0.00001,
    Quote.NZDJPY: 0.001,
    Quote.NZDUSD: 0.00001,
    Quote.USDCAD: 0.00001,
    Quote.USDCHF: 0.00001,
    Quote.USDJPY: 0.001
}

__annual_bars_of = {
    Timeframe.D1: 261,
    Timeframe.H4: 261*6,
    Timeframe.H1: 261*24,
    Timeframe.M20: 261*24*3,
}

class IndexRange:
    def __init__(self, start:int, exclusive_end:int):
        self.start = start
        self.end = exclusive_end

    def sliced_of(self, l):
        return l[self.start:self.end]

class Index:
    def __init__(self, irange:IndexRange, local_index:int):
        self.local = local_index
        if irange:
            self.glob = irange[0] + local_index
        else:
            self.glob = local_index

class EntryIndices:
    def __init__(self):
        self.__idx = []
        self.__type = []

    def append(self, i:Index, pos_type:PosType):
        self.__type.append(pos_type)
        self.__idx.append(i)

    def __getitem__(self, i):
        return self.__type[i], self.__idx[i]
    
    def size(self):
        return len(self.__idx)

