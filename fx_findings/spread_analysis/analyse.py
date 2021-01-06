from ..base.enums import Timeframe, Quote, Broker, Col
from ..base import loader
from ..base import utils

str_of_weekday = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']

def analyse_time_based_spread(timeframe:Timeframe, quote:Quote, broker:Broker):
    df = loader.load(timeframe, quote, broker)
    time_based_spread = dict()
    col_datetime = df[Col.DATETIME]
    col_spread = df[Col.SPREAD]

    for datetime, spread in zip(col_datetime, col_spread):
        if timeframe == Timeframe.D1:
            weekday = datetime.weekday()
            key = str_of_weekday[weekday]
        else: # assume hours based
            key = datetime.hour
        
        if key in time_based_spread:
            time_based_spread[key].append(spread)
        else:
            time_based_spread[key] = [spread]

    for key in time_based_spread.keys():
        l = time_based_spread[key]
        time_based_spread[key] = utils.avg(l)

    return time_based_spread
            
            
            

def analyse_broker_spread_ratio(timeframe:Timeframe, quote:Quote, broker:Broker):
    df = loader.load(timeframe, quote)
    tickstory_spread = utils.average_spread(df)
    tickstory_len = len(df)

    df = loader.load(timeframe, quote, broker)
    broker_spread = utils.average_spread(df)
    broker_len = len(df)

    print('(unit in points)')
    print('tickstory', '----------', f'{tickstory_len} {tickstory_spread:.2f}')
    print('broker   ', f'{broker:10s}', f'{broker_len} {broker_spread:.2f}')
    print(f'{broker:s}/tickstory ratio => {broker_spread/tickstory_spread:.2f}')
    return broker_spread/tickstory_spread, tickstory_spread, broker_spread

def run():
    ratio, base_spread, broke_spread = analyse_broker_spread_ratio(Timeframe.H1, Quote.AUDCAD, Broker.XM)
    time_based_spread = analyse_time_based_spread(Timeframe.H1, Quote.AUDCAD, Broker.XM)

    print('Time-based avg spread', Timeframe.H1)
    for key, val in time_based_spread.items():
        print(key, val)