from .enums import Quote, Col

def average_spread(df):
    series = df[Col.SPREAD]
    return sum(series)/len(series)

def avg(l):
    return sum(l)/len(l)

__point_size_of = {
        Quote.AUDCAD: 0.00001
    }

def point_size(quote:Quote):
    return __point_size_of[quote]

def pip_size(quote:Quote):
    return point_size(quote)*10