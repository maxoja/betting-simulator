from ..base.enums import Timeframe, Quote, Broker
from ..base import loader
from ..base import utils

def analyse_spread(timeframe:Timeframe, quote:Quote, broker:Broker):
    df = loader.load(timeframe, quote)
    tickstory_spread = utils.average_spread(df)
    tickstory_len = len(df)

    df = loader.load(timeframe, quote, broker)
    broker_spread = utils.average_spread(df)
    broker_len = len(df)

    print('(unit in points)')
    print('tickstory', '----------', f'{tickstory_len} {tickstory_spread:.2f}')
    print('broker   ', f'{broker:10s}', f'{broker_len} {broker_spread:.2f}')
    return broker_spread

def run():
    analyse_spread(Timeframe.H1, Quote.AUDCAD, Broker.XM)