from .enums import Quote, Col, Timeframe


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


__point_size_of = {
    Quote.AUDCAD: 0.00001
}

__annual_bars_of = {
    Timeframe.D1: 261,
    Timeframe.H4: 261*6,
    Timeframe.H1: 261*24
}