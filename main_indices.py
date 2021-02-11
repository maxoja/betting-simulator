from sys import argv
import numpy as np
from fx_findings.base.enums import *
from fx_findings import currency_indices
from fx_findings.base import plotting
from fx_findings.base import loader
from fx_findings.base import utils

agg_gbp = currency_indices.run('GBP')
agg_aud = currency_indices.run('AUD')

agg_gbp += 100
agg_aud += 100

reproduced_gbpaud = agg_gbp/agg_aud*100

df, meta = loader.load(Timeframe.D1, Quote.GBPAUD, None)
body_series = df[Col.BODY]*utils.point_size(meta.quote)
open_series = df[Col.OPEN]
prop_change = body_series/open_series*100
original_gbpaud = np.cumsum(prop_change) + 100

# plotting.plot_lines([change1, change2, main_line, change1/change2*100], 'GBP, AUD, main')
# plotting.plot_lines([main_line, change1/change2*100])
plotting.plot_lines([original_gbpaud], 'GBPAUD')

plotting.block()