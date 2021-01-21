from ..base.enums import Timeframe, Quote, Broker, Col
from ..base import loader
from ..base import utils
from ..base import plotting

str_of_weekday = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']

def analyse_weekday_spread(timeframe:Timeframe, quote:Quote, broker:Broker):
    df = loader.load(timeframe, quote, broker)
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

    spread_avg = utils.avg_dict(spread_values)
    return utils.sorted_dict(spread_avg)

def analyse_time_spread(timeframe:Timeframe, quote:Quote, broker:Broker, weekday=None):
    df = loader.load(timeframe, quote, broker)
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

    spread_avg = utils.avg_dict(spread_values)
    return utils.sorted_dict(spread_avg)
            

def analyse_broker_spread_ratio(timeframe:Timeframe, quote:Quote, broker:Broker):
    df = loader.load(timeframe, quote, None)
    tickstory_spread = utils.average_spread(df)
    tickstory_len = len(df)

    df = loader.load(timeframe, quote, broker)
    broker_spread = utils.average_spread(df)
    broker_len = len(df)

    print('(unit in points)')
    print('tickstory', '----------', f'{tickstory_len} {tickstory_spread:.2f}')
    print('broker   ', f'{broker:10s}', f'{broker_len} {broker_spread:.2f}')
    print(f'{broker:s}/tickstory ratio => {broker_spread/tickstory_spread:.2f}')
    return broker_spread/tickstory_spread, tickstory_spread, broker_spread


def run():
    TARGET_BROKER = Broker.XM_LOW
    TARGET_QUOTE = Quote.AUDCAD
    TARGET_TIMEFRAME = Timeframe.M20

    ratio, base_spread, broke_spread = analyse_broker_spread_ratio(TARGET_TIMEFRAME, TARGET_QUOTE, TARGET_BROKER)

    day_spread_broke = analyse_weekday_spread(TARGET_TIMEFRAME, TARGET_QUOTE, TARGET_BROKER)
    plotting.plot_dict_as_bars(day_spread_broke, title="Day Spread - {TARGET_BROKER}")

    for i in [0, 1, 3, 4]:
        time_spread_broke = analyse_time_spread(TARGET_TIMEFRAME, TARGET_QUOTE, TARGET_BROKER, i)
        if len(time_spread_broke.keys()) > 0:
            plotting.plot_dict_as_bars(time_spread_broke, title=f"{str_of_weekday[i]} - Time Spread - {TARGET_BROKER}")

    plotting.block()
