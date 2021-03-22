from ..enums import Quote, Col, Timeframe

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


def average_spread(df):
    series = df[Col.SPREAD]
    return sum(series)/len(series)


def point_size(quote:Quote):
    return __point_size_of[quote]


def pip_size(quote:Quote):
    return point_size(quote)*10


def annual_bars(timeframe:Timeframe):
    return __annual_bars_of[timeframe]

