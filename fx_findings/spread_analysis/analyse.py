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

    print('tickstory', '----------', tickstory_len, tickstory_spread)
    print('broker   ', f'{broker:10s}', broker_len, broker_spread)

def run():
    analyse_spread(Timeframe.H1, Quote.AUDCAD, Broker.XM)