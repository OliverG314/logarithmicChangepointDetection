# logarithmicChangepointDetection
A Python library containing 5 methods to count and locate certain changes in logarithmic data, as well as an algorithm to generate the data.

# Generating the data
There are 6 parameters for calling ```genData(k, n, S, T, F, theta, seed)```, as well as a parameter for the seed. $k$ and $n$ are used to generate the x-values; $\textbf{X} = (k, 2k, ..., nk)$. $S$ represents the location of steps. $T$ represents any additional shifts for each step, with a default of no additional shifts. $F$ represents the random noise to be added, with a default of uniform, and theta represents the parameters, with a default of (0, 1).

```python
from genData import genData

data = genData(0.1, 1000, [500])
```

# Algorithms
## Interval gradient method
This method splits the data up and calculates the gradient of a linear regression for each subset of data. Where the slope exceeds a threshold, a step is detected.

## Total gradient method
This method considers total gradients up to an increasing number of x-values, and detects a step at a local minimum

## KDE method
This method counts steps by counting the number of local maxima in a kernel density estimate of y-values, and subtracts 1

## F statistic method
This method looks at the fit of 

```python
from logChangeDetect import intervalGradientMethod
from genData import genData

data = genData(0.1, 1000, [500])

change = intervalGradientMethod(data)

steps = change.countSteps()
locs  = change.locSteps()
```
