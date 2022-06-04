import statistics
import math
import re
import matplotlib.pyplot as plt

def getDataFromFile(fileAddress,expectedNumber,mode=1):
    with open(fileAddress, 'r') as file:
        fileText = file.read()
    if mode == 1:
        indexes = [m.start() for m in re.finditer('Mbits/sec', fileText)]
    else:
        indexes = [m.start() for m in re.finditer('MBytes', fileText)]
    if len(indexes) != expectedNumber:
        print("FALSE")
        return []
    data = []
    for i in range(len(indexes)):
        data.append(float(fileText[indexes[i] - 7:indexes[i] - 1]))
    return data

def getErrorBarData(data,t = 2.086): # for 50 is 2.009 if we calculate 20 times t is 2.086
    standardDeviation = statistics.stdev(data)
    squareData = math.sqrt(len(data))
    return t * (standardDeviation / squareData)

def draw(dataNdimension):
    means = []
    confidences = []
    for i in range(len(dataNdimension)):
        confidence = getErrorBarData(dataNdimension[i])
        dataMean = statistics.mean(dataNdimension[i])
        means.append(dataMean)
        confidences.append(confidence)
    # print(range(len(dataNdimension)))
    print(means)
    print(confidences)
    plt.errorbar([20,40,60,80,100], means, yerr=confidences)
    plt.title('Bandwidth of lia and fullmesh')
    plt.xlabel("B link delay")
    plt.ylabel("Bandwidth of H3-H4")
    plt.show()

def getDataNdimension(fileAddressList,expectedNumber):
    dataNdimension = []
    for i in range(len(fileAddressList)):
        oneData = getDataFromFile(fileAddressList[i],expectedNumber,1)
        if len(oneData) == 0:
            print("FALSE FALSE")
            return
        dataNdimension.append(oneData)
    return dataNdimension
    
fileAddressList = ['resultH4-20ms-mode5.txt','resultH4-40ms-mode5.txt','resultH4-60ms-mode5.txt','resultH4-80ms-mode5.txt','resultH4-100ms-mode5.txt']
dataNdimension = getDataNdimension(fileAddressList,20)
# print(dataNdimension)
draw(dataNdimension)
