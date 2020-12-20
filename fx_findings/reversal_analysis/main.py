import matplotlib.pyplot as plt
import numpy
import talib

from ..base.enums import Timeframe, Quote, Col, Broker
from ..base import loader
from ..base import utils

def average_spread(df):
    series = df[Col.SPREAD]
    return sum(series)/len(series)


def analyse_spread(timeframe:Timeframe, quote:Quote, broker:Broker):
    df = loader.load(timeframe, quote)
    tickstory_spread = average_spread(df)
    tickstory_len = len(df)

    df = loader.load(timeframe, quote, broker)
    broker_spread = average_spread(df)
    broker_len = len(df)

    print('tickstory', '----------', tickstory_len, tickstory_spread)
    print('broker   ', f'{broker:10s}', broker_len, broker_spread)

def analyse_rsi_reversal(timeframe:Timeframe, quote:Quote, broker:Broker=None, limit=None, shift=0, plot=True):
    RSI_PERIOD = 14
    OVER_THRESH = 70
    UNDER_THRESH = 30
    FUTURE_PERIOD = 2
    
    df = loader.load(timeframe, quote, broker)
    if not limit is None:
        df = df[(-limit-RSI_PERIOD-shift):len(df)-shift]
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
        utils.plot_histogram_unblock(over_future_changes)
        utils.plot_histogram_unblock(under_future_changes)
        utils.plot_centered_cumulative_histogram(over_future_changes)
        utils.plot_centered_cumulative_histogram(under_future_changes)
        plt.show()
    
    
def main():
    # analyse_spread(Timeframe.H1, Quote.AUDCAD, Broker.XM)
    analyse_rsi_reversal(Timeframe.D1, Quote.AUDCAD)
    # for i in range(10):
    #     analyse_rsi_reversal(Timeframe.D1, Quote.AUDCAD, limit=180, shift=180*i, plot=False)
    #     print('-'*10)
    # print('===========')
    # for i in range(10):
    #     analyse_rsi_reversal(Timeframe.H4, Quote.AUDCAD, limit=60*6, shift=60*i*6, plot=False)
    #     print('-'*10)

