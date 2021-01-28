You should be careful about whether or not to shift indicator series produced from TALib. As the indicator values are produced from ending price (close) of bars, **if your strategy open trades before a bar is closed**, the indicator point of that bar won't be fully formed yet and you would need to shift the indicator series to the right to match bars with most recent available indicator points.

```
import talib
import numpy as np

close_series = np.array([1.0, 0.0, 3.0, 2.0, 3.0])
print(talib.RSI(close_series, 2))

# RSI(2) uses 3 bars
>>> [nan, nan, 75., 50., 70.]
```
