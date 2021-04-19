from ..enums import Quote, Col, Timeframe

YEARLY_TRADING_DAYS = 252

__annual_bars_of = {
    Timeframe.D3: YEARLY_TRADING_DAYS//3,
    Timeframe.D2: YEARLY_TRADING_DAYS//2,
    Timeframe.D1: YEARLY_TRADING_DAYS,
    Timeframe.H4: YEARLY_TRADING_DAYS*6,
    Timeframe.H1: YEARLY_TRADING_DAYS*24,
    Timeframe.M20: YEARLY_TRADING_DAYS*24*3,
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

