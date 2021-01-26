import numpy as np
import talib
import pandas as pd

from ..base.enums import Timeframe, Quote, Col, Broker, PosType, Direction, Clr
from ..base import loader
from ..base import utils
from ..base import plotting

def run(timeframe:Timeframe=Timeframe.D1, quote:Quote=Quote.USDJPY, pos_type:PosType=PosType.LONG):
    df, meta = loader.load(timeframe, quote)
    bars_2_years = 2*utils.annual_bars(timeframe)
    if len(df) > bars_2_years:
        df = utils.slice_frame1(df, bars_2_years)
    data_size = len(df)

    wick_t = df[Col.WICK_T]
    wick_b = df[Col.WICK_B]
    rise = df[Col.RISE]
    fall = df[Col.FALL]
    body = df[Col.BODY]
    height = df[Col.HEIGHT].to_numpy()

    min_rise, max_rise = min(rise), max(rise)
    thresh_range = range(int(min_rise)+50, int(max_rise+1), 100)
    # thresh_range = [250, 300, 350, 400, 450, 500, 550]
    # thresh_range = [300]
    x1 = []
    y1 = []
    for entry_min_risefall in thresh_range:
        if pos_type is PosType.LONG:
            entry_idx = fall >= entry_min_risefall
            selected_bodies = body[entry_idx]
            profits = entry_min_risefall + selected_bodies
        else:
            entry_idx = rise >= entry_min_risefall
            selected_bodies = body[entry_idx]
            profits = entry_min_risefall - selected_bodies

        gain_idx = profits > 0
        loss_idx = ~gain_idx
            
        # datetime = df[Col.DATETIME][entry_idx]
        # rsi_val = rsi_5[entry_idx]
        # print(pd.concat([datetime, rsi_val], axis=1))
        
        s = f"OvergrownThresh={entry_min_risefall} avgGain={utils.avg(profits):.02f} x {len(profits)}"
        background = Clr.LIGHT_RED if pos_type is PosType.SHORT else Clr.LIGHT_BLUE
        plotting.plot_histogram(profits, title=s)

        # for rsi_period in [14, 10, 6]:
        for rsi_period in [14]:
            rsi = talib.RSI(df[Col.CLOSE], rsi_period)
            rsi = utils.shift_right_with_nan(rsi)

            entry_rsi = rsi[entry_idx]
            gain_rsi = entry_rsi[gain_idx]
            loss_rsi = entry_rsi[loss_idx]
            gain_rsi = utils.remove_nan(gain_rsi)
            loss_rsi = utils.remove_nan(loss_rsi)

            acc_dir = Direction.RIGHT if pos_type is PosType.SHORT else Direction.LEFT
            best_rsi = plotting.plot_threshold_cross_cumulation(gain_rsi, loss_rsi, acc_dir, background, title=f'RSI PERIOD={rsi_period} ENTRY={entry_min_risefall}')
            # plotting.plot_threshold_cross_cumulation(gain_rsi_buy, loss_rsi_buy, title=f'BUY RSI PERIOD={rsi_period} ENTRY={entry_min_risefall}')
            # plotting.plot_histogram(gain_rsi, title=f"RSI-{rsi_period} of gains (avg {utils.avg(gain_rsi):.02f} med {np.median(gain_rsi):.02f})")
            # plotting.plot_histogram(loss_rsi, color='red', title=f"RSI-{rsi_period} of loss (avg {utils.avg(loss_rsi):.02f} med {np.median(loss_rsi):.02f})")
        
        prev_entry_idx = utils.shift_left(entry_idx, False)
        entry_height = height[prev_entry_idx]
        if entry_idx[0] == True:
            tmp_gain_idx = gain_idx[1:]
            tmp_loss_idx = loss_idx[1:]
            gain_height = entry_height[tmp_gain_idx]
            loss_height = entry_height[tmp_loss_idx]
        else:
            gain_height = entry_height[gain_idx]
            loss_height = entry_height[loss_idx]

        best_height_r = plotting.plot_threshold_cross_cumulation(gain_height, loss_height, Direction.RIGHT, background, title=f'HEIGHT >>>> ENTRY={entry_min_risefall}')
        best_height_l = plotting.plot_threshold_cross_cumulation(gain_height, loss_height, Direction.LEFT, background, title=f'HEIGHT <<<< ENTRY={entry_min_risefall}')
        
        plotting.block()

    plotting.plot_histogram(body, title=f'{quote} {timeframe} Body Sizes (points): {data_size}')
    plotting.block()