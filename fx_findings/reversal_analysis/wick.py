import numpy as np
import talib

from ..base.enums import Timeframe, Quote, Col, Broker, PosType
from ..base import loader
from ..base import utils
from ..base import plotting

def destructure_candles(df, quote:Quote):
    top, bot, body, shirt, pants = [], [], [], [], []
    point_size = utils.point_size(quote)
    zipped_ohcl = zip(df[Col.OPEN]/point_size, df[Col.CLOSE]/point_size, df[Col.HIGH]/point_size, df[Col.LOW]/point_size)

    for op, cl, hi, lo in zipped_ohcl:
        sorted_prices = sorted([op, cl])
        top += [hi-sorted_prices[-1]]
        bot += [sorted_prices[0]-lo]
        body += [cl - op]
        shirt += [hi - op]
        pants += [op - lo]

    return np.array(top), np.array(bot), np.array(shirt), np.array(pants), np.array(body)

def run():
    QUOTE = Quote.AUDCAD
    TIMEFRAME = Timeframe.D1

    df = loader.load(TIMEFRAME, QUOTE)
    data_size = len(df)
    top_wicks, bot_wicks, shirts, pants, bodies = destructure_candles(df, QUOTE)

    min_shirt, max_shirt = min(shirts), max(shirts)
    x1 = []
    y1 = []
    for min_entry_dist in range(int(min_shirt), int(max_shirt+1), 50):
        arg_ = shirts >= min_entry_dist
        x1.append(min_entry_dist)
        selected_bodies = bodies[arg_]
        profits = -1*selected_bodies + min_entry_dist
        plotting.plot_histogram(profits, title=f"{min_entry_dist} avg {utils.avg(profits)} x {len(profits)}")
        plotting.block()
        # print(profits)
        # print(utils.avg(profits))
        # y1.append(utils.avg(profits))
        y1.append(profits)

    plotting.plot_boxes(y1, x1)
    # print(y1[0])
    # y1 = tuple(y1)
    # plotting.plot_scatter(x1, y1)
    plotting.block()

    
    plotting.plot_histogram(top_wicks, title=f'{QUOTE} {TIMEFRAME} Top Wick Sizes (points): {data_size}')
    plotting.plot_histogram(bot_wicks, title=f'{QUOTE} {TIMEFRAME} Bot Wick Sizes (points): {data_size}')
    plotting.plot_histogram(bodies, title=f'{QUOTE} {TIMEFRAME} Body Sizes (points): {data_size}')
    plotting.block()