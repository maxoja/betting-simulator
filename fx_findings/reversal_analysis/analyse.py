import numpy
import talib

from ..base.enums import Timeframe, Quote, Col, Broker
from ..base import loader
from ..base import utils
from ..base import plotting

RSI_PERIOD = 14
OVER_THRESH = 70
UNDER_THRESH = 30
FUTURE_PERIOD = 2

def analyse_rsi_reversal(df, quote, plot=True):
    
    close_series = df[Col.CLOSE].reset_index(drop=True)
    rsi_series = talib.RSI(close_series, RSI_PERIOD)
    
    over_future_changes = []
    under_future_changes = []
    for i in range(len(rsi_series)):
        current_rsi = rsi_series[i]

        if numpy.isnan(current_rsi):
            continue
        if len(rsi_series) - i <= FUTURE_PERIOD:
            continue

        current_close = close_series[i]
        future_close = close_series[i+FUTURE_PERIOD]
        future_change_points = (future_close - current_close)/utils.point_size(quote)

        if current_rsi >= OVER_THRESH:
            over_future_changes.append(future_change_points)
        if current_rsi <= UNDER_THRESH:
            under_future_changes.append(future_change_points)

    total_over = len(over_future_changes)
    total_under = len(under_future_changes)
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
    quote = Quote.AUDCAD
    df = loader.load(Timeframe.D1, quote)
    analyse_rsi_reversal(df, quote)
    exit()
    for i in range(10):
        sliced_df = utils.slice_frame(df, 180, shift=180*i, buffer=RSI_PERIOD)
        if sliced_df is None:
            break
        analyse_rsi_reversal(sliced_df, quote, plot=False)
        print('-'*10)
    print('===========')
    for i in range(10):
        sliced_df = utils.slice_frame(df, 60*6, shift=60*6*i, buffer=RSI_PERIOD)
        if sliced_df is None:
            break
        analyse_rsi_reversal(sliced_df, quote, plot=False)
        print('-'*10)

