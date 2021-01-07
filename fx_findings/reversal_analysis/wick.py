import numpy as np
import talib

from ..base.enums import Timeframe, Quote, Col, Broker, PosType
from ..base import loader
from ..base import utils
from ..base import plotting

def destructure_candles(df, quote:Quote):
    top, bot, body = [], [], []
    point_size = utils.point_size(quote)
    zipped_ohcl = zip(df[Col.OPEN]/point_size, df[Col.CLOSE]/point_size, df[Col.HIGH]/point_size, df[Col.LOW]/point_size)

    for op, cl, hi, lo in zipped_ohcl:
        sorted_prices = sorted([op, cl, hi, lo])
        top += [sorted_prices[-1]-sorted_prices[-2]]
        bot += [sorted_prices[1]-sorted_prices[0]]
        body += [cl - op]

    return top, bot, body

def run():
    QUOTE = Quote.AUDCAD
    TIMEFRAME = Timeframe.D1

    df = loader.load(TIMEFRAME, QUOTE)
    data_size = len(df)
    top_wicks, bot_wicks, bodies = destructure_candles(df, QUOTE)
    plotting.plot_histogram(top_wicks, title=f'{QUOTE} {TIMEFRAME} Top Wick Sizes (points): {data_size}')
    plotting.plot_histogram(bot_wicks, title=f'{QUOTE} {TIMEFRAME} Bot Wick Sizes (points): {data_size}')
    plotting.plot_histogram(bodies, title=f'{QUOTE} {TIMEFRAME} Body Sizes (points): {data_size}', block=True)