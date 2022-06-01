import statistics
import math
import re
import matplotlib.pyplot as plt

def getDataFromFile(fileAddress,expectedNumber):
    with open(fileAddress, 'r') as file:
        fileText = file.read()
    indexes = [m.start() for m in re.finditer('Mbits/sec', fileText)]
    if len(indexes) != expectedNumber:
        print("FALSE")
        return []
    data = []
    for i in range(len(indexes)):
        data.append(float(data[indexes[i] - 7:indexes[i] - 1]))
    return data

def getErrorBarData(data,t = 2.009): # for 50 if we calculate 20 times t is 2.086
    standardDeviation = statistics.stdev(data)
    squareData = math.sqrt(len(data))
    return t * (standardDeviation / squareData)

def draw(dataNdimension):
    means = []
    confidences = []
    for i in range(dataNdimension):
        confidence = getErrorBarData(dataNdimension[i])
        dataMean = statistics.mean(dataNdimension[i])
    plt.errorbar(range(len(dataNdimension)), means, yerr=confidences)
    plt.title('errorbar function Example')
    plt.show()

def getDataNdimension(fileAddressList,expectedNumber):
    dataNdimension = []
    for i in range(len(fileAddressList)):
        oneData = getDataFromFile(fileAddressList[i],expectedNumber)
        if len(oneData) == 0:
            print("FALSE FALSE")
            return
        dataNdimension.append(oneData)
    return dataNdimension
    
fileAddressList = ['resultH2-20ms.txt']
dataNdimension = getDataNdimension(fileAddressList,1)
draw(dataNdimension)
