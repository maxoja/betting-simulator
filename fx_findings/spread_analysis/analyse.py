from ..base.enums import Timeframe, Quote, Broker, Col
from ..base import loader
from ..base import plotting
from ..utils import arith as arith_utils
from ..utils import market as utils_market
from ..utils import pandas as utils_pandas

str_of_weekday = ['0-Mon', '1-Tue', '2-Wed', '3-Thu', '4-Fri', '5-Sat', '6-Sun']

def analyse_weekday_spread(timeframe:Timeframe, quote:Quote, broker:Broker):
    df, meta = loader.load_price_dataset(timeframe, quote, broker)
    df = utils_pandas.slice_frame_from_back(df, utils_market.annual_bars(timeframe)//2)
    spread_values = dict()
    col_datetime = df[Col.DATETIME]
    col_spread = df[Col.SPREAD]

    for datetime, spread in zip(col_datetime, col_spread):
        weekday = datetime.weekday()
        key = str_of_weekday[weekday]
         
        if key in spread_values:
            spread_values[key].append(spread)
        else:
            spread_values[key] = [spread]

    spread_avg = arith_utils.avg_dict(spread_values)
    return arith_utils.sorted_dict(spread_avg)

def analyse_time_spread(timeframe:Timeframe, quote:Quote, broker:Broker, weekday=None):
    df, meta = loader.load_price_dataset(timeframe, quote, broker)
    df = utils_pandas.slice_frame_from_back(df, utils_market.annual_bars(timeframe)//2)
    spread_values = dict()
    col_datetime = df[Col.DATETIME]
    col_spread = df[Col.SPREAD]

    for datetime, spread in zip(col_datetime, col_spread):
        if not weekday is None and datetime.weekday() != weekday:
            continue
        key = f'{datetime.hour:02d}{datetime.minute:02d}'

        if key in spread_values:
            spread_values[key].append(spread)
        else:
            spread_values[key] = [spread]

    spread_avg = arith_utils.avg_dict(spread_values)
    return arith_utils.sorted_dict(spread_avg)
            

def analyse_broker_spread_ratio(timeframe:Timeframe, quote:Quote, broker:Broker):
    df, meta = loader.load_price_dataset(timeframe, quote, None)
    df = utils_pandas.slice_frame_from_back(df, utils_market.annual_bars(timeframe)//2)
    tickstory_spread = utils_market.average_spread(df)
    tickstory_len = len(df)

    df, meta = loader.load_price_dataset(timeframe, quote, broker)
    df = utils_pandas.slice_frame_from_back(df, utils_market.annual_bars(timeframe)//2)
    broker_spread = utils_market.average_spread(df)
    broker_len = len(df)

    print('(unit in points)')
    print('tickstory', '----------', f'{tickstory_len} {tickstory_spread:.2f}')
    print('broker   ', f'{broker:10s}', f'{broker_len} {broker_spread:.2f}')
    print(f'{broker:s}/tickstory ratio => {broker_spread/tickstory_spread:.2f}')
    return broker_spread/tickstory_spread, tickstory_spread, broker_spread


def run(TARGET_TIMEFRAME:Timeframe, TARGET_QUOTE:Quote, TARGET_BROKER:Broker):
    # TARGET_BROKER = Broker('xm-low')
    # TARGET_QUOTE = Quote.AUDCAD
    # TARGET_TIMEFRAME = Timeframe.M20

    # ratio, base_spread, broke_spread = analyse_broker_spread_ratio(TARGET_TIMEFRAME, TARGET_QUOTE, TARGET_BROKER)

    day_spread_broke = analyse_weekday_spread(TARGET_TIMEFRAME, TARGET_QUOTE, TARGET_BROKER)
    plotting.plot_dict_as_bars(day_spread_broke, title=f"Day Spread - {TARGET_BROKER}")

    for i in [0, 1, 3, 4]:
        time_spread_broke = analyse_time_spread(TARGET_TIMEFRAME, TARGET_QUOTE, TARGET_BROKER, i)
        if len(time_spread_broke.keys()) > 0:
            plotting.plot_dict_as_bars(time_spread_broke, title=f"{str_of_weekday[i]} - Time Spread - {TARGET_BROKER}")

    plotting.block()

def run_all(TARGET_TIMEFRAME:Timeframe, TARGET_BROKER:Broker):
    structured_result = {}

    for pair in Quote:
        spread_of_time = analyse_time_spread(TARGET_TIMEFRAME, pair, TARGET_BROKER)
        spreads = spread_of_time.values()
        spreads = sorted(spreads)
        # min_spread, max_spread = min(spreads), max(spreads)
        percentile_85 = spreads[len(spreads)*85//100]
        print(pair, percentile_85)
        # print(pair, min_spread, percentile_80, max_spread)
        structured_result[''+pair] = percentile_85

    print(structured_result)
