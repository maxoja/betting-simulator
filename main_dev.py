from pandas import DataFrame
from fx_findings.base import utils

data = {'number': [1,2,3,4,5,6]}
df = DataFrame(data)
print(df)

print(utils.slice_frame1(df, 3, 1))
print(utils.slice_frame2(df, 2, 3, 1))