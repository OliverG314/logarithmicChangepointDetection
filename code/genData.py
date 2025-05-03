import pandas as pd
import numpy  as np

import matplotlib        as mpl
import matplotlib.pyplot as plt

def p(X, S, T):
    logValues = []

    for i in range(len(X)):
        xVal = np.round(X[i], 12)

        idx = np.searchsorted(S*X[0], xVal)

        value = np.log(np.prod(S[1:idx]) * (xVal - X[0]*S[idx-1])/X[0]) + T[idx - 1]

        if value < 0:
            print(xVal, value)

        logValues.append(value)

    return logValues

def genData(k, n, S, T=None, F="unif", theta={"low":0, "high":1}, seed=None):
    if seed != None:
        np.random.seed(seed)
        
    X = np.linspace(k, n*k, n)

    S = np.array(S)

    if S[0] != 0: S = np.insert(S, 0, 0)
    if S[-1] != X[-1]/X[0]: np.append(S, X[-1]/X[0])

    if T == None: T = [0 for i in range(len(S))]
    
    T = np.array(T)

    if F == "unif": F = np.random.uniform
    if F == "norm":
        F = np.random.normal
        
        if theta == {"low":0, "high":1}:
            theta = {"loc":0, "scale":1}

    epsilon = F(**theta, size=n)

    Y = p(X, S, T) + epsilon

    df = pd.DataFrame(list(zip(X, Y)), columns=["x", "y"])

    return df
