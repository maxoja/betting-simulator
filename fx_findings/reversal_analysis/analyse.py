import numpy
import talib

from ..base.enums import Timeframe, Quote, Col, Broker
from ..base import loader
from ..base import utils
from ..base import plotting

OUTPUT_DIR = './out/rsi_reversal/'
RSI_PERIOD = 14
OVER_THRESH = 70
UNDER_THRESH = 30
FUTURE_PERIOD = 2

class Config:
    def __init__(self, quote, timeframe, rsi_period, padding_thresh, future_window):
        self.quote = quote
        self.timeframe = timeframe
        self.rsi_period = rsi_period
        self.padding_thresh = padding_thresh
        self.future_window = future_window

    def as_str(self):
        return f'quote={self.quote}|timeframe={self.timeframe}|rsi_period={self.rsi_period}|padding={self.padding_thresh}|future_win={self.future_window}'

def entry_points_rsi_reversal(df, config:Config, irange:utils.IndexRange=None) -> utils.EntryIndices:
    sliced_df = irange.sliced_of(df) if irange else df
    close_series = sliced_df[Col.CLOSE].reset_index(drop=True)
    rsi_series = talib.RSI(close_series, config.rsi_period)

    buy_entries = []
    sell_entries = []

    entries = utils.EntryIndices()

    for i in range(len(rsi_series)):
        current_rsi = rsi_series[i]

        if numpy.isnan(current_rsi):
            continue

        if current_rsi >= 100-config.padding_thresh:
            entries.buy.append(utils.Index(irange, i))
        if current_rsi <= config.padding_thresh:
            entries.sell.append(utils.Index(irange, i))

    return entries

def analyse_rsi_reversal(df, config:Config, plot=True):
    
    close_series = df[Col.CLOSE].reset_index(drop=True)
    rsi_series = talib.RSI(close_series, config.rsi_period)
    
    over_future_changes = []
    under_future_changes = []
    for i in range(len(rsi_series)):
        current_rsi = rsi_series[i]

        if numpy.isnan(current_rsi):
            continue
        if len(rsi_series) - i <= config.future_window:
            continue

        current_close = close_series[i]
        future_close = close_series[i+config.future_window]
        future_change_points = (future_close - current_close)/utils.point_size(config.quote)

        if current_rsi >= 100-config.padding_thresh:
            over_future_changes.append(future_change_points)
        if current_rsi <= config.padding_thresh:
            under_future_changes.append(future_change_points)

    n_bars = len(close_series)-config.rsi_period
    n_years = n_bars/utils.annual_bars(config.timeframe)
    total_over = len(over_future_changes)
    total_under = len(under_future_changes)

    print(config.as_str())
    print('# Bars', n_bars, f'# Years {n_years:.2f}')
    if total_over > 0:
        print('overbought', total_over, utils.avg(over_future_changes))
    if total_under > 0:
        print('oversold  ', total_under, utils.avg(under_future_changes))
    if total_over > 0 and total_under > 0:
        print('weighted  ', total_over+total_under, utils.avg(list(map(lambda x: -x, over_future_changes)) + under_future_changes) )
    
    if plot:
        plotting.plot_histogram_unblock(over_future_changes)
        plotting.plot_histogram_unblock(under_future_changes)
        plotting.plot_centered_cumulative_histogram(over_future_changes)
        plotting.plot_centered_cumulative_histogram(under_future_changes)
        plotting.show_plot()
    
    
def run():
    PARAM_PERIOD = [14]
    PARAM_FUTURE_WIN = [1,2,3]
    PARAM_PADDING = [26,28,30,32,34]
    
    for period in PARAM_PERIOD:
        for padding in PARAM_PADDING:
            for future_win in PARAM_FUTURE_WIN:
                conf = Config(Quote.AUDCAD, Timeframe.D1, period, padding, future_win)
                df = loader.load(conf.timeframe, conf.quote)
                analyse_rsi_reversal(df, conf, plot=False)
                print()