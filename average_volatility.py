import sys

from fx_findings.base import loader
from fx_findings.base import utils
from fx_findings.base.enums import Quote, Timeframe, Col
from fx_findings.base import plotting

N_YEAR = 1
N_SLICE = 3

target_timeframe = Timeframe(sys.argv[1])
target_quote = Quote(sys.argv[2])
target_broker = None

df, meta = loader.load_price_dataset(target_timeframe, target_quote, target_broker)
n_bar = N_YEAR*utils.market.annual_bars(meta.timeframe)//N_SLICE
n_shift = n_bar

avg_dicts = []

for slice_set in range(N_SLICE):
    sliced_df = utils.pandas.slice_frame_from_back(df, n_bar, slice_set*n_shift)

    avg_volat = {}

    for datetime, body in zip(sliced_df[Col.DATETIME], sliced_df[Col.BODY]):
        if meta.timeframe == Timeframe.D1:
            chunk_key = utils.time.weekday_str(datetime)
        else:
            chunk_key = utils.time.hour_minute_str(datetime)

        if not chunk_key in avg_volat:
            avg_volat[chunk_key] = []

        avg_volat[chunk_key].append(abs(body))

    avg_volat = utils.arith.avg_dict(avg_volat)
    avg_volat = utils.arith.sorted_dict(avg_volat)
    avg_dicts.append(avg_volat)
    
plotting.plot_dict_as_line(avg_dicts, f"Average volatility {target_quote} {target_timeframe} ({N_SLICE} slices from {N_YEAR} years)")

plotting.block()