from math import *
from PySA import PySA
from random import *

seed()

# merge two path loss
def Merge(db1, db2):
    C_MAXDB = 600
    C_MLN10 = -0.23025850929940456840179914546844
    C_EPSILON = 0.001
    if db1 < 0:
        return db2
    if db2 < 0:
        return db1
    if db1 >= C_MAXDB:
        t1 = 0
    elif db1 < C_EPSILON:
        t1 = 1
    else:
        t1 = exp(db1 * C_MLN10)
    if db2 >= C_MAXDB:
        t2 = 0
    elif db2 <= C_EPSILON:
        t2 = 1
    else:
        t2 = exp(db2 * C_MLN10)
    t1 += t2
    if t1 >= 1:
        return 0
    elif t1 > 0:
        return -10 * log10(t1)
    else:
        return min(abs(db1), abs(db2))

def dot(v1, v2):
    return sum([a * b for a, b in zip(v1, v2)])

# free space path loss in dB
def FreeSpace(km, MHz):
    return 20 * log10(km) + 20 * log10(MHz) + 32.44

# Freq = 3.5 WiMAX
MHz = 3500

# multipaths
paths = []

# number of paths
np = randint(5, 20) 

for i in range(0, np):
    # link distance, reflection, diffraction, transmission
    cur = [(random() + 0.001), randint(0, 7),
           randint(0, 7),
           randint(0, 7)]
    paths.append(cur)

def getDB(paths, MHz, mat):
    meas = 600
    for i in paths:
        db = FreeSpace(i[0], MHz) + i[1] * dot(i[1:], mat)
        meas = Merge(meas, db)
        #if db < meas:
        #    meas = db
    return meas
    
# material variable
mat = [5, 5, 5]
meas = getDB(paths, MHz, mat)
print meas

# calibration engine
SA = PySA()

bestE = curE = newE = 9999
bestS = curS = newS = []

def genNew():
    global newE, newS, paths, MHz, mat, meas, bestS, bestE, curE, curS
    newS = [randint(0, 20), randint(0, 20), randint(0, 20)]
    newE = abs(getDB(paths, MHz, newS) - meas)
    bestS = newS
    bestE = newE
    curE = bestE
    curS = newS
    return newE

def genNB():
    global newS, curS, newE, paths, MHz, newS, meas
    newS = curS
    newS[randint(0, 2)] = randint(0, 100) * 0.1
    newE = abs(getDB(paths, MHz, newS) - meas)
    return newE
    
def accNB():
    global curS, newS, curE, newE, bestE, bestS
    curS = newS
    curE = newE
    if curE < bestE:
        bestE = curE
        bestS = curS
        
SA.generateNew = genNew
SA.generateNB = genNB
SA.acceptNB = accNB
SA.Prepare()

while not SA.Step():
    #print SA.Temperature
    pass

print bestS, ' ', bestE
print getDB(paths, MHz, bestS)
print mat
print getDB(paths, MHz, mat)

