from pandas import DataFrame
from fx_findings.base import utils
from fx_findings.base.enums import Quote

data = {'number': [i for i in range(1,11)]}
df = DataFrame(data)

print('original')
print(df)
print()

print('slice from back\nsize=3, shift=1, buffer=0')
print(utils.pandas.slice_frame_from_back(df, 3, 1))
print()

print('slice from back\nsize=2, shift=3, buffer=1')
print(utils.pandas.slice_frame_from_front(df, 2, 3, 1))
print()

print(utils.market.point_size(Quote.AUDJPY))
print(utils.market.point_size(Quote.EURJPY))
print(utils.market.point_size(Quote.AUDNZD))
print()