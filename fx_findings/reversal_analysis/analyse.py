import numpy
import talib

from ..base.enums import Timeframe, Quote, Col, Broker, PosType
from ..base import loader
from ..base import utils
from ..base import plotting

OUTPUT_DIR = './out/rsi_reversal/'
RSI_PERIOD = 14
OVER_THRESH = 70
UNDER_THRESH = 30
FUTURE_PERIOD = 2

class Settings:
    def __init__(self, quote, timeframe, rsi_period, padding_thresh):
        self.quote = quote
        self.timeframe = timeframe
        self.rsi_period = rsi_period
        self.padding_thresh = padding_thresh

    def as_str(self):
        return f'quote={self.quote}|timeframe={self.timeframe}|rsi_period={self.rsi_period}|padding={self.padding_thresh}'

# entry at index i mean you open a trade after the bar at index i is closed
def entry_points_rsi_reversal(df, settings:Settings, irange:utils.IndexRange=None) -> utils.EntryIndices:
    sliced_df = irange.sliced_of(df) if irange else df
    close_series = sliced_df[Col.CLOSE].reset_index(drop=True)
    rsi_series = talib.RSI(close_series, settings.rsi_period)

    buy_entries = []
    sell_entries = []

    entries = utils.EntryIndices()

    for i in range(len(rsi_series)):
        current_rsi = rsi_series[i]

        if numpy.isnan(current_rsi):
            continue

        if current_rsi >= 100-settings.padding_thresh:
            entries.append(utils.Index(irange, i), PosType.LONG)
        if current_rsi <= settings.padding_thresh:
            entries.append(utils.Index(irange, i), PosType.SHORT)

    return entries

# def analyse_rsi_reversal(df, settings:Settings, plot=True):
    
#     close_series = df[Col.CLOSE].reset_index(drop=True)
#     rsi_series = talib.RSI(close_series, settings.rsi_period)
    
#     short_diff = []
#     long_diff = []
#     for i in range(len(rsi_series)):
#         current_rsi = rsi_series[i]

#         if numpy.isnan(current_rsi):
#             continue
#         if len(rsi_series) - i <= settings.future_window:
#             continue

#         current_close = close_series[i]
#         future_close = close_series[i+settings.future_window]
#         future_change_points = (future_close - current_close)/utils.point_size(settings.quote)

#         if current_rsi >= 100-settings.padding_thresh:
#             short_diff.append(future_change_points)
#         if current_rsi <= settings.padding_thresh:
#             long_diff.append(future_change_points)

#     n_bars = len(close_series)-settings.rsi_period
#     n_years = n_bars/utils.annual_bars(settings.timeframe)
#     total_short = len(short_diff)
#     total_long = len(long_diff)

#     print(settings.as_str())
#     print('# Bars', n_bars, f'# Years {n_years:.2f}')
#     if total_short > 0:
#         print('overbought', total_short, utils.avg(short_diff))
#     if total_long > 0:
#         print('oversold  ', total_long, utils.avg(long_diff))
#     if total_short > 0 and total_long > 0:
#         print('weighted  ', total_short+total_long, utils.avg(list(map(lambda x: -x, short_diff)) + long_diff) )
    
#     if plot:
#         plotting.plot_histogram_unblock(short_diff)
#         plotting.plot_histogram_unblock(long_diff)
#         plotting.plot_centered_cumulative_histogram(short_diff)
#         plotting.plot_centered_cumulative_histogram(long_diff)
#         plotting.show_plot()
    
def analyse_position_progression(df, entries:utils.EntryIndices, win_size=1, plot=True):
    close = df[Col.CLOSE]

    long_diff = []
    short_diff = []

    for i in range(entries.size()):
        pos_type, entry_i = entries[i]

        if entry_i.glob + win_size >= len(df):
            continue

        start_price = close[entry_i.glob]
        end_price = close[entry_i.glob + win_size]
        diff = end_price - start_price

        if pos_type == PosType.LONG:
            long_diff.append(diff)
        else:
            short_diff.append(diff)

    total_short = len(short_diff)
    total_long = len(long_diff)

    if total_short > 0:
        print('shorts', total_short, utils.avg(short_diff))
    if total_long > 0:
        print('longs  ', total_long, utils.avg(long_diff))
    if total_short > 0 and total_long > 0:
        print('weighted  ', total_short+total_long, utils.avg(list(map(lambda x: -x, short_diff)) + long_diff) )
    
    if plot:
        plotting.plot_histogram_unblock(short_diff)
        plotting.plot_histogram_unblock(long_diff)
        plotting.plot_centered_cumulative_histogram(short_diff)
        plotting.plot_centered_cumulative_histogram(long_diff)
        plotting.show_plot()

def run():
    PARAM_PERIOD = [14]
    # PARAM_FUTURE_WIN = [1,2,3]
    PARAM_PADDING = [26,28,30,32,34]
    
    for period in PARAM_PERIOD:
        for padding in PARAM_PADDING:
        # for future_win in PARAM_FUTURE_WIN:
            settings = Settings(Quote.AUDCAD, Timeframe.D1, period, padding)
            df = loader.load(settings.timeframe, settings.quote)
            entries = entry_points_rsi_reversal(df, settings, None)
            analyse_position_progression(df, entries)
            # analyse_rsi_reversal(df, settings, plot=False)
            print()