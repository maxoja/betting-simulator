import numpy as np

from ..base.enums import Timeframe, Quote, Broker, Col
from ..base import loader
from ..base import plotting
from ..base import utils

relatives = {
    'GBP' : ['GBPJPY', 'GBPUSD', 'GBPCAD', 'GBPNZD', 'GBPCHF'],
    'AUD' : ['AUDJPY', 'AUDUSD', 'AUDCAD', 'AUDNZD', 'AUDCHF']
}

def run(currency='GBP'):
    timeframe = Timeframe.D1
    broker = None
    frames, metas = [], []
    quotes = relatives[currency]

    for quote in quotes:
        dataframe, meta = loader.load_price_dataset(timeframe, quote, broker)
        frames.append(dataframe)
        metas.append(meta)

    merged_chage = None
    plotting_lines = []
    for dataframe, meta in zip(frames, metas):
        # close_series = dataframe[Col.CLOSE]
        # plotting.plot_lines([close_series], 'Close series of ' + meta.quote)
        body_series = dataframe[Col.BODY] * utils.market.point_size(meta.quote) # convert from points to price
        open_series = dataframe[Col.OPEN]
        percent_change_series = body_series / open_series * 100
        # plotting.plot_lines([percent_change_series], 'Percent change of ' + meta.quote)
        # plotting.block()

        if merged_chage is None:
            merged_chage = percent_change_series/len(quotes)
        else:
            merged_chage += percent_change_series/len(quotes)

        individual_movement = np.cumsum(percent_change_series)
        plotting_lines.append(individual_movement)

    merged_movement = np.cumsum(merged_chage)
    # plotting.plot_lines([merged_movement], 'Avergage percentage change of ' + str(quotes))
    # plotting.block()

    # plotting_lines = [merged_movement] + individual_movement
    plotting_lines = [merged_movement]
    plotting.plot_lines(plotting_lines, 'aggregated movement of'+currency)

    return merged_chage

# closes = []
# for i, quote in enumerate(quotes):
#     meta = metas[i]
#     df = dfs[i]
#     close_series = df[Col.CLOSE]
#     min_val = min(close_series)
#     max_val = max(close_series)
#     range_val = max_val - min_val
#     normalised = (close_series-min_val)/range_val
#     normalised = normalised - normalised[0]
#     closes.append(normalised)

# plotting.plot_lines(closes)

# changes = None
# originals = []
# for i, quote in enumerate(quotes):
#     meta = metas[i]
#     df = dfs[i]
#     body_series = df[Col.BODY]
#     avgBody = utils.avg(np.abs(body_series))
#     body_series = body_series/avgBody

#     if changes is None:
#         changes = body_series/len(quotes)
#     else:
#         changes += body_series/len(quotes)

#     originals.append(np.cumsum(body_series))

# changes = np.cumsum(changes)
# plotting.plot_lines([changes] + originals)