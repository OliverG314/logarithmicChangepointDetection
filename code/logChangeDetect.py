import numpy  as np
import pandas as pd

import warnings
import sys

from genData import genData

import matplotlib        as mpl
import matplotlib.pyplot as plt

np.random.seed(0)

def linReg(x, y):
    if len(x) != len(y): raise Exception("x and y different lengths. len(x) = " + str(len(x)) + ", len(y) = " + str(len(y)))

    n = len(x)

    xBar = sum(x)/n
    yBar = sum(y)/n

    Sxx = sum([(x[i] - xBar)**2            for i in range(n)])
    Sxy = sum([(x[i] - xBar)*(y[i] - yBar) for i in range(n)])

    b = Sxy/Sxx
    a = yBar - b*xBar

    return a, b

def sma(x, k=1):
    n = len(x)
    
    smaList = np.zeros(n)
    
    for i in range(1,n):
        data = x[:i]
        
        smaList[i] = sum(data)/len(data)

    smaList[:k]  = smaList[k]
    smaList[-k:] = smaList[-k-1]

    return smaList

class intervalGradientMethod:
    def __init__(self, data, intW = 20, thresh = None):
        self.data = data
        self.intW = intW

        if len(self.data["y"])/self.intW != len(self.data["y"])//self.intW:
            raise Exception("Interval width does not divide data length. Interval width = " + str(self.intW) + ", data length = " + str(len(self.data["y"])))

        self.threshold = thresh
        
        if thresh == None: self.threshold = 1.5/(intW*k)

        plt.style.use("ggplot")

        mpl.rc("font", **{"family": "CMU Serif",
                      "size":   12})
        
    def getSlopes(self):
        y = self.data["y"]

        slopes = []
        
        for i in range(len(y)//self.intW):
            intData = self.data.iloc[i*self.intW:(i+1)*self.intW]

            x = intData["x"].tolist()
            y = intData["y"].tolist()

            a, b = linReg(x, y)

            slopes.append(b)

        return slopes

    def countSteps(self):
        self.slopes = self.getSlopes()

        self.steps = len([i for i in self.slopes if i > self.threshold]) - 1

        return self.steps

    def locSteps(self):
        self.slopes = self.getSlopes()

        self.locs = self.data["x"].iloc[[i*self.intW for i in range(len(self.slopes)) if self.slopes[i] > self.threshold]].index.tolist()

        self.locs = [[i, i+self.intW] for i in self.locs]

        return self.locs

    def plot(self):
        plt.scatter(self.data["x"], self.data["y"], color="black", s=10, label="Data")

        plt.axhline(self.threshold, color="blue", alpha=0.5, linestyle="dashed", label="Threshold")

        slopes = []

        for i in range(len(self.data["y"])//self.intW):
            intData = self.data.iloc[i*self.intW:(i+1)*self.intW]

            x = intData["x"].tolist()
            y = intData["y"].tolist()

            a, b = linReg(x, y)

            slopes.append(b)

            plt.plot(x, a + b*np.array(x), color="darkorange", solid_capstyle="round")
            plt.axvline((i+1)*self.intW*k, color="grey", alpha=0.5)

        plt.axvline(0, color="grey", alpha=0.5, label="Interval boundaries")
        
        plt.scatter(self.intW*self.data["x"].iloc[0]/2 + np.arange(0, max(self.data["x"]), max(self.data["x"])/len(slopes)), slopes, s=10,
                    color = [["red", "springgreen"][i > self.threshold] for i in slopes])

        plt.xlabel("X", weight="bold")
        plt.ylabel("Y", weight="bold")

        plt.title("Interval gradient method, w = " + str(self.intW))

        plt.plot(0, 0, color="darkorange", solid_capstyle="round", label="Interval gradients")

        plt.scatter(self.intW*self.data["x"].iloc[0]/2, slopes[0], s=10, color="red", label="Gradient [no step]")
        plt.scatter(self.intW*self.data["x"].iloc[0]/2, slopes[0], s=10, color="springgreen", label="Gradient [step]")

        plt.legend(loc="center right", fontsize="small")

        yTicks      = plt.yticks()[0]
        yTickLabels = [str(tick).replace("\u2212", "-") for tick in yTicks]

        plt.yticks(yTicks, yTickLabels)

    def savePlot(self, fileName):
        mng = plt.get_current_fig_manager()

        mng.full_screen_toggle()

        plt.gca().margins(x=0.05, y=0.05)

        plt.savefig(f"imgs/{fileName}.pdf", bbox_inches="tight")

class totalGradientMethod:
    def __init__(self, data, intW = 20, slopeDiffThresh = None):
        self.data = data
        self.intW = intW

        if slopeDiffThresh == None: self.slopeDiffThresh = 0.001

        plt.style.use("ggplot")

        mpl.rc("font", **{"family": "CMU Serif",
                      "size":   12})

    def getSlopes(self):
        y = self.data["y"]

        slopes = []

        for i in range(len(y)//self.intW):
            intData = self.data.iloc[:(i+1)*self.intW]

            x = intData["x"].tolist()
            y = intData["y"].tolist()

            a, b = linReg(x, y)

            slopes.append(b)

        return slopes

    def countSteps(self):
        self.slopes = self.getSlopes()

        self.steps = np.zeros(len(self.slopes))

        for i in range(1, len(self.slopes)-1):
            lower = self.slopes[i] - self.slopes[i-1]
            upper = self.slopes[i] - self.slopes[i+1]
            
            if lower < 0 and upper < 0:
                if abs(lower) > self.slopeDiffThresh and abs(upper) > self.slopeDiffThresh:
                    self.steps[i] = 1

        return sum(self.steps)

    def locSteps(self):
        self.countSteps()

        locs = []

        for i in range(len(self.steps)):
            if self.steps[i]:
                locs.append((i+1)*self.intW)

        locs = [[i, i+self.intW] for i in locs]

        return locs

    def plot(self):
        plt.scatter(self.data["x"], self.data["y"], color="black", s=10, label="Data")

        interc = []
        slopes = []

        for i in range(len(self.data["y"])//self.intW):
            intData = self.data.iloc[:(i+1)*self.intW]

            x = intData["x"].tolist()
            y = intData["y"].tolist()

            a, b = linReg(x, y)

            interc.append(a)
            slopes.append(b)

            plt.plot(x, a + b*np.array(x), color="darkorange", solid_capstyle="round")
            plt.axvline((i+1)*self.intW*k, color="grey", alpha=0.5)

        self.countSteps()

        for i in range(len(self.steps)):
            if self.steps[i]:
                x = self.data.iloc[:(i+1)*self.intW]["x"]
                
                plt.plot(x, interc[i] + slopes[i]*x, color="springgreen")

        plt.xlabel("X", weight="bold")
        plt.ylabel("Y", weight="bold")

        plt.title("Total gradient method, w = " + str(self.intW))

    def savePlot(self, fileName):
        mng = plt.get_current_fig_manager()

        mng.full_screen_toggle()

        plt.gca().margins(x=0.05, y=0.05)

        plt.savefig(f"imgs/{fileName}.pdf", bbox_inches="tight")

class kdeMethod:
    def __init__(self, data, h=0.5, nKDE=1000):
        self.data = data
        self.h    = h
        self.nKDE = nKDE

        self.kde = self.getKDE(self.data["y"], self.h)

        plt.style.use("ggplot")

        mpl.rc("font", **{"family": "CMU Serif",
                      "size":   12})

    def countSteps(self):
        steps = []
        
        maxVals = self.countMax(self.kde, k=10)

        for i in range(len(maxVals)):
            if maxVals[i]:
                steps.append(i)

        steps.pop(-1)

        self.steps = steps

        return len(steps)

    def locSteps(self):
        self.countSteps()

        return self.steps

    def countMax(self, y, k=1):
        n = len(y)
        
        isMax = np.zeros(n)
        
        for i in range(k, n-k):
            if max(y[i-k:i+k+1]) == y[i]:
                isMax[i] = 1

        return isMax

    def getKDE(self, y, h):
        kdeVals = [self.kde(i, y, h) for i in np.linspace(min(y), max(y), self.nKDE)]

        return kdeVals

    def kde(self, yVal, y, h):
        return 1/(len(y) * h) * np.sum(self.w((yVal - y)/h))

    def w(self, u):
        return 1/np.sqrt(2*np.pi) * np.exp(-(u**2)/2)

    def plot(self):
        y = self.data["y"]
        
        plt.hist(y, density=True, bins=30, color="slategrey", label="y values")

        plt.plot(np.linspace(min(y), max(y), self.nKDE), self.kde, color="red", label="KDE")

        plt.legend()

        plt.xlabel("y")
        plt.ylabel("Density")
        
        plt.title("Histogram of y values")

    def savePlot(self, fileName):
        mng = plt.get_current_fig_manager()

        mng.full_screen_toggle()

        plt.gca().margins(x=0.05, y=0.05)

        plt.savefig(f"imgs/{fileName}.pdf", bbox_inches="tight")

class totalFStatMethod:
    def __init__(self, data, step=10):
        self.data = data
        self.step = step

        self.xRange = np.arange(self.step, len(self.data["x"]), self.step)

    def countSteps(self):
        self.fStats = self.getFStats()

        self.fSMA = self.sma(self.fStats)

        self.steps = self.locMax(self.fSMA)

        return len(self.steps)

    def locSteps(self):
        return self.steps

    def locMax(self, x, k=1):
        peaks = []
        
        for i in range(k, len(x)-k):
            if max(x[i-k:i+k+1]) == x[i]:
                peaks.append(i)

        return peaks

    def sma(self, x, k=1):
        n = len(x)
        
        sma = np.zeros(n-2*k)

        sma = np.insert(sma, 0, np.array(x[:k]))
        
        for i in range(k, n-k):
            data = x[i-k:i+k+1]
            
            sma[i] = sum(data)/len(data)

        sma = np.append(sma, x[-k:])

        return sma

    def getFStats(self):
        fStats = []
        
        for i in self.xRange:
            dfHead = self.data.head(i)

            fStat = self.fStat(dfHead)

            fStats.append(fStat)

        return fStats

    def fStat(self, df):
        x = df["x"]
        y = df["y"]

        n = len(x)

        yBar = sum(y)/n

        yFitted = self.fittedValues(np.log(x), y)

        SSR = sum([(yFitted[i] - yBar)**2 for i in range(n)])
        SSE = sum([(y[i] - yFitted[i])**2 for i in range(n)])

        f = SSR/(SSE/(n-2))

        return f
    
    def fittedValues(self, x, y):
        n = len(x)

        xBar = sum(x)/n
        yBar = sum(y)/n

        Sxx = sum([(x[i]-xBar)**2 for i in range(n)])
        Sxy = sum([(x[i]-xBar)*(y[i]-yBar) for i in range(n)])

        b = Sxy/Sxx
        a = yBar - b*xBar

        return b*x + a

    def plot(self):
        self.countSteps()

        plt.scatter(self.xRange, self.fStats, color="black", label="F statistic for model up to x-value")
        plt.plot(self.xRange, self.fSMA, color="red", label="Simple moving average")

        plt.xlabel("X")
        plt.ylabel("F statistic")

        plt.title("F statistics for linear model of y~ln(x), increasing by " + str(self.step) + " x-values")

        plt.legend()

    def savePlot(self, fileName):
        mng = plt.get_current_fig_manager()

        mng.full_screen_toggle()

        plt.gca().margins(x=0.05, y=0.05)

        plt.savefig(f"imgs/{fileName}.pdf", bbox_inches="tight")
                
n = 1000
k = 0.1
S = [500]

data = genData(k, n, S, theta={"low":0, "high":1})

i = intervalGradientMethod(data)

i.plot()

print(i.countSteps())
print(i.locSteps())

plt.show()
