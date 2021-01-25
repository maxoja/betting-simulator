import numpy as np
from .enums import Quote, Col, Timeframe, PosType


def slice_frame1(df, size, shift_end=0, buffer=0):
    if shift_end < 0 or size+buffer+shift_end >= len(df):
        return None
        
    start = (-size-shift_end-buffer)
    end = len(df)-shift_end
    return df[start:end]


def slice_frame2(df, size, shift_front=0, buffer=0):
    start = shift_front - buffer
    end = shift_front + size
    return df[start:end]


def average_spread(df):
    series = df[Col.SPREAD]
    return sum(series)/len(series)


def avg(l):
    return sum(l)/len(l)


def avg_dict(d):
    return {key:avg(val) for key,val in d.items()}


def point_size(quote:Quote):
    return __point_size_of[quote]


def pip_size(quote:Quote):
    return point_size(quote)*10


def annual_bars(timeframe:Timeframe):
    return __annual_bars_of[timeframe]


def sorted_dict(d):
    return { k:d[k] for k in sorted(d.keys()) }


def shift_right_with_nan(a):
    a = np.concatenate(([np.NaN], a))
    a = a[:-1]
    return a

def remove_nan(a):
    non_nan_idx = np.isnan(a)
    return a[~non_nan_idx]

__point_size_of = {
    Quote.AUDCAD: 0.00001,
    Quote.EURCHF: 0.00001,
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

    


