# logarithmicChangepointDetection
A Python library containing 4 methods to detect certain changes in logarithmic data, as well as an algorithm to generate the data.

# Generating the data
There are 6 parameters for calling ```genData(k, n, S, T, F, theta, seed)```. $k$ and $n$ are used to generate the x-values; $\textbf{X} = (k, 2k, ..., nk)$.

```python
from genData import genData

data = genData(
```

# Algorithms
## Interval gradient method
