from math import *
from PySA import PySA
from random import *

seed()
C_MAXDB = 600
C_MLN10 = -0.23025850929940456840179914546844
C_EPSILON = 0.001

# merge two path loss
def Merge(db1, db2):
    global C_MAXDB, C_MLN10, C_EPSILON
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

# Freq = GSM 900
MHz = 947

# multipaths
paths = []

# number of meas points
np = 50

for nm in range(0, np):
    mpaths = []
    # number of paths
    np = randint(1, 25) 

    for i in range(0, np):
        # link distance, reflection, diffraction, transmission
        cur = [(random() + 0.001), randint(0, 7),
               randint(0, 7),
               randint(0, 7)]
        mpaths.append(cur)
        
    paths.append(mpaths)

def getDB(mpaths, MHz, mat):
    global C_MAXDB
    meas = C_MAXDB
    for i in mpaths:
        db = FreeSpace(i[0], MHz) + i[1] * dot(i[1:], mat)
        meas = Merge(meas, db)
        #if db < meas:
        #    meas = db
    return meas

def getDBs(paths, MHz, mat):
    meas = []
    for i in paths:
        meas.append(getDB(i, MHz, mat))
    return meas

def RMSE(v1, v2):
    v = [x - y for x, y in zip(v1, v2)]
    s = sum([x ** 2 for x in v])
    return sqrt(s / min(len(v1), len(v2)))    
    
# material variable
mat = [5, 5, 5]
meas = getDBs(paths, MHz, mat)

# calibration engine
SA = PySA()

bestE = curE = newE = 9999
bestS = []
curS = []
newS = []

def genNew():
    global newE, newS, paths, MHz, mat, meas, bestS, bestE, curE, curS
    newS = [randint(0, 20), randint(0, 20), randint(0, 20)]
    print 'Initial solution: ', newS
    newE = RMSE(getDBs(paths, MHz, newS), meas)
    bestS = [x for x in newS]
    bestE = newE
    curE = bestE
    curS = [x for x in newS]
    return newE

def genNB():
    global newS, curS, newE, paths, MHz, newS, meas
    newS = [x for x in curS]
    newS[randint(0, 2)] = randint(0, 100) * 0.1
    newE = RMSE(getDBs(paths, MHz, newS), meas)
    return newE
    
def accNB():
    global curS, newS, curE, newE, bestE, bestS
    curS = [x for x in newS]
    curE = newE
    if curE < bestE:
        bestE = curE
        bestS = [x for x in curS]
        
SA.generateNew = genNew
SA.generateNB = genNB
SA.acceptNB = accNB
SA.Prepare()

print "Simulated Annealing Running ..."
fp = open("statistics.csv", "w")

while not SA.Step():
    fp.write(str(SA.Temperature) + "," + str(SA.CurrentEnergy) + chr(13))

fp.close()
print bestS, ' ', bestE
print RMSE(getDBs(paths, MHz, bestS), meas)
