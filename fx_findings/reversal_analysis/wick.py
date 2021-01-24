import numpy as np
import talib
import pandas as pd

from ..base.enums import Timeframe, Quote, Col, Broker, PosType
from ..base import loader
from ..base import utils
from ..base import plotting

def destructure_candles(df, df_meta:loader.Meta):
    point_size = utils.point_size(df_meta.quote)
    wick_t, wick_b, body, rise, fall = [], [], [], [], []
    zipped_ohcl = zip(df[Col.OPEN]/point_size, df[Col.CLOSE]/point_size, df[Col.HIGH]/point_size, df[Col.LOW]/point_size)

    for op, cl, hi, lo in zipped_ohcl:
        sorted_prices = sorted([op, cl])
        wick_t += [hi-sorted_prices[-1]]
        wick_b += [sorted_prices[0]-lo]
        body += [cl - op]
        rise += [hi - op]
        fall += [op - lo]

    df[Col.WICK_T] = wick_t
    df[Col.WICK_B] = wick_b
    df[Col.RISE] = rise
    df[Col.FALL] = fall
    df[Col.BODY] = body

    return np.array(wick_t), np.array(wick_b), np.array(rise), np.array(fall), np.array(body)

def run():
    QUOTE = Quote.AUDCAD
    TIMEFRAME = Timeframe.D1

    df, meta = loader.load(TIMEFRAME, QUOTE)
    bars_2_years = 2*utils.annual_bars(TIMEFRAME)
    if len(df) > bars_2_years:
        df = utils.slice_frame1(df, bars_2_years)
    data_size = len(df)
    top_wicks, bot_wicks, rise, fall, body = destructure_candles(df, meta)
    rsi_14 = talib.RSI(df[Col.CLOSE], 14)
    rsi_5 = np.concatenate(([np.NaN],rsi_14))
    rsi_7 = talib.RSI(df[Col.CLOSE], 7)
    rsi_5 = np.concatenate(([np.NaN],rsi_7))
    rsi_5 = talib.RSI(df[Col.CLOSE], 5)
    rsi_5 = np.concatenate(([np.NaN],rsi_5))
    rsi_5 = rsi_5[:-1]
    rsi_7 = rsi_7[:-1]
    rsi_14 = rsi_14[:-1]

    min_rise, max_rise = min(rise), max(rise)
    thresh_range = range(int(min_rise)+50, int(max_rise+1), 100)
    thresh_range = [250, 300, 350, 400, 450]
    # thresh_range = [300]
    x1 = []
    y1 = []
    for entry_min_rise in thresh_range:
        entry_idx = rise >= entry_min_rise
        # entry_idx = np.logical_and(entry_idx, rsi_5 < 40)
        # datetime = df[Col.DATETIME][entry_idx]
        # rsi_val = rsi_5[entry_idx]
        # print(pd.concat([datetime, rsi_val], axis=1))
        # print(datetime)
        x1.append(entry_min_rise)
        selected_bodies = body[entry_idx]
        profits = entry_min_rise - selected_bodies
        gain_idx = profits > 0
        loss_idx = ~gain_idx
        
        s = f"{entry_min_rise} avg {utils.avg(profits):.02f} x {len(profits)}"
        plotting.plot_histogram(profits, title=s)
        print(s)

        for rsi_period in [14, 7, 5]:
            rsi = talib.RSI(df[Col.CLOSE], rsi_period)
            rsi = np.concatenate(([np.NaN],rsi))
            rsi = rsi[:-1]
            entry_rsi = rsi[entry_idx]
            gain_rsi = entry_rsi[gain_idx]
            gain_rsi = gain_rsi[~np.isnan(gain_rsi)]
            loss_rsi = entry_rsi[loss_idx]
            loss_rsi = loss_rsi[~np.isnan(loss_rsi)]

            print('RSI PERIOD =', rsi_period, 'ENTRY =', entry_min_rise)
            print('-'*10)
            for percentile in range(10,100,10):
                print(f'RSI gain {percentile}% -> {np.percentile(gain_rsi, percentile):.2f}')
            print('-'*10)
            for percentile in range(10,100,10):
                print(f'RSI loss {percentile}% -> {np.percentile(loss_rsi, percentile):.2f}')
            print()
            plotting.plot_cross_cumulative(gain_rsi, loss_rsi, title=f'RSI PERIOD ={rsi_period} ENTRY ={entry_min_rise}')
            # plotting.plot_histogram(gain_rsi, title=f"RSI-{rsi_period} of gains (avg {utils.avg(gain_rsi):.02f} med {np.median(gain_rsi):.02f})")
            # plotting.plot_histogram(loss_rsi, color='red', title=f"RSI-{rsi_period} of loss (avg {utils.avg(loss_rsi):.02f} med {np.median(loss_rsi):.02f})")
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
    plotting.plot_histogram(body, title=f'{QUOTE} {TIMEFRAME} Body Sizes (points): {data_size}')
    plotting.block()