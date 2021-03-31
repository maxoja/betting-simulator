import sys

from fx_findings.base.enums import Quote, Timeframe, Col
from fx_findings.base import loader
from fx_findings.base import plotting
from fx_findings.base import utils

N_YEAR = 2
N_SLICE = 4

timeframe = Timeframe(sys.argv[1])
quote = Quote(sys.argv[2])
broker = None

df, meta = loader.load_price_dataset(timeframe, quote, broker)
n_bar = utils.market.annual_bars(meta.timeframe)*N_YEAR//N_SLICE
n_shift = n_bar

avg_dicts = []

for i_slice in range(N_SLICE):
    sliced_df = utils.pandas.slice_frame_from_back(df, n_bar, n_shift*i_slice)
    avg_dif = {}

    for datetime, body, height, wick_t in zip(sliced_df[Col.DATETIME], sliced_df[Col.BODY], sliced_df[Col.HEIGHT], sliced_df[Col.WICK_T]):
        if body == 0:
            continue
        if height < 150:
            continue
        if meta.timeframe == Timeframe.D1:
            chunk_key = utils.time.weekday_str(datetime)
        else:
            chunk_key = utils.time.hour_minute_str(datetime)

        if not chunk_key in avg_dif:
            avg_dif[chunk_key] = []

        diff = height-abs(body)
        avg_dif[chunk_key].append(diff)

    avg_dif = utils.arith.avg_dict(avg_dif)
    avg_dif = utils.arith.sorted_dict(avg_dif)
    avg_dicts.append(avg_dif)

plotting.plot_dict_as_line(avg_dicts, f"Average range - volat diff {quote} {timeframe} ({N_SLICE} slices from {N_YEAR} years)")
plotting.block()
    
