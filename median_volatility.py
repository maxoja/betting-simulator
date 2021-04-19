import sys

from fx_findings.base import loader
from fx_findings.base import utils
from fx_findings.base.enums import Quote, Timeframe, Col
from fx_findings.base import plotting

N_YEAR = 2
N_SLICE = 4

target_timeframe = Timeframe(sys.argv[1])
target_quote = Quote(sys.argv[2])
target_broker = None

df, meta = loader.load_price_dataset(target_timeframe, target_quote, target_broker)
print(df[:10])
n_bar = N_YEAR*utils.market.annual_bars(meta.timeframe)//N_SLICE
n_shift = n_bar

avg_dicts = []
dicts = []

for slice_set in range(N_SLICE):
    sliced_df = utils.pandas.slice_frame_from_back(df, n_bar, slice_set*n_shift)

    volats = {}

    for datetime, body in zip(sliced_df[Col.DATETIME], sliced_df[Col.BODY]):
        if meta.timeframe.daily_or_larger():
            chunk_key = utils.time.weekday_str(datetime)
        else:
            chunk_key = utils.time.hour_minute_str(datetime)

        if not chunk_key in volats:
            volats[chunk_key] = []

        volats[chunk_key].append(abs(body))

    volats = utils.arith.sorted_dict(volats)
    dicts.append(volats)

print(dicts)

plotting.plot_dicts_as_stacked_ribbons_of_median(dicts, 0.1, f"Median volatility {target_quote} {target_timeframe} ({N_SLICE} slices from {N_YEAR} years) (err={0.1})")
merged_dicts = utils.arith.sorted_dict(utils.arith.merge_dict_of_lists(dicts))
plotting.plot_dicts_as_stacked_ribbons_of_median(merged_dicts, 0.25, f"Median volatility {target_quote} {target_timeframe} ({N_YEAR} years) (err={0.25})")


plotting.block()