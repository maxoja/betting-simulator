from ..enums import Quote, Col, Timeframe

__annual_bars_of = {
    Timeframe.D1: 261,
    Timeframe.H4: 261*6,
    Timeframe.H1: 261*24,
    Timeframe.M20: 261*24*3,
}


def average_spread(df):
    series = df[Col.SPREAD]
    return sum(series)/len(series)


def point_size(quote:Quote):
    if 'JPY' in (''+quote):
        return 0.001
    return 0.00001


def pip_size(quote:Quote):
    return point_size(quote)*10


def annual_bars(timeframe:Timeframe):
    return __annual_bars_of[timeframe]

