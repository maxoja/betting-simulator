from .enums import Quote, Col, Timeframe, PosType


def slice_frame(df, size, shift=0, buffer=0):
    if shift < 0 or size+buffer+shift >= len(df):
        return None
        
    print('->', size+buffer, len(df), '->', (-size-shift-buffer), len(df)-shift)
    return df[(-size-shift-buffer):len(df)-shift]


def average_spread(df):
    series = df[Col.SPREAD]
    return sum(series)/len(series)


def avg(l):
    return sum(l)/len(l)


def point_size(quote:Quote):
    return __point_size_of[quote]


def pip_size(quote:Quote):
    return point_size(quote)*10


def annual_bars(timeframe:Timeframe):
    return __annual_bars_of[timeframe]


def sorted_dict(d):
    return { k:d[k] for k in sorted(d.keys()) }


__point_size_of = {
    Quote.AUDCAD: 0.00001,
    Quote.EURCHF: 0.00001
}

__annual_bars_of = {
    Timeframe.D1: 261,
    Timeframe.H4: 261*6,
    Timeframe.H1: 261*24
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

    


