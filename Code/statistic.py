import statistics
import math
import matplotlib.pyplot as plt

def getErrorBarData(data,t = 2.009): # for 50 if we calculate 20 times t is 2.086
    standardDeviation = statistics.stdev(data)
    squareData = math.sqrt(len(data))
    return t * (standardDeviation / squareData)

def draw(data):
    confidence = getErrorBarData(data)
    dataMean = statistics.mean(data)
    plt.errorbar([1], dataMean, yerr=confidence)
    plt.title('errorbar function Example')
    plt.show()