# logarithmicChangepointDetection
A Python library containing 4 methods to detect certain changes in logarithmic data, as well as an algorithm to generate the data.

# Generating the data
There are 6 parameters for calling ```genData(k, n, S, T, F, theta, seed)```, as well as a parameter for the seed. $k$ and $n$ are used to generate the x-values; $\textbf{X} = (k, 2k, ..., nk)$. $S$ represents the location of steps. $T$ represents any additional shifts for each step, with a default of no additional shifts. $F$ represents the random noise to be added, with a default of uniform, and theta represents the parameters, with a default of (0, 1).

```python
from genData import genData

data = genData(0.1, 1000, [500])
```

# Algorithms
## Interval gradient method
