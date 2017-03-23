import json
import numpy as np
from tqdm import tqdm
import pandas as pd
import time
import csv
import scipy
from scipy.stats import pearsonr
from scipy.spatial import distance

mapUidToDayDict = {}
mapUidToHourDict = {}
mapUidToMonthDict = {}
uniqueUser = set()

with open('./facts.json') as f_in:
    for line in tqdm(f_in):
        j = json.loads(line.strip())
        dayDict = {i : 0 for i in range(7)}
        hrDict = {i : 0 for i in range(24)}
        monthDict = {i : 0 for i in range(1,13)}
        uid = j["uid"]
        for timestamp in j["facts"]:
        	dayDict[time.gmtime(timestamp["ts"] / 1000.0).tm_wday] += 1
            hrDict[time.gmtime(timestamp["ts"] / 1000.0).tm_hour] += 1 
            monthDict[time.gmtime(timestamp["ts"] / 1000.0).tm_mon] += 1

        if uid in mapUidToDayDict:
            for i in dayDict:
                mapUidToDayDict[uid][i] += dayDict[i]
        else:
            mapUidToDayDict[uid] = dayDict

        if uid in mapUidToHourDict:
            for i in hrDict:
                mapUidToHourDict[uid][i] += hrDict[i]
        else:
            mapUidToHourDict[uid] = hrDict

        if uid in mapUidToMonthDict:
            for i in monthDict:
                mapUidToMonthDict[uid][i] += monthDict[i]
        else:
            mapUidToMonthDict[uid] = monthDict


def cross_entropy(t1, t2):
    entropy = 0
    for i in range(7):
        if t1[i] == 0 or t2[i] == 0: continue
        entropy -= t1[i] * math.log(t2[i], 2)
    return entropy

print "start cal coef"
cnt = 0;
f = open('DayHourMonth.csv', 'wt')
writer = csv.writer(f)
with open('./Knnlist.csv') as f_in:
    for line in tqdm(f_in):
        u = line.strip().split(',')
        if (u[0], u[1]) in uniqueUser:
            continue
        d0 = mapUidToDayDict[u[0]].values()
        d1 = mapUidToDayDict[u[1]].values()
        h0 = mapUidToHourDict[u[0]].values()
        h1 = mapUidToHourDict[u[1]].values()
        m0 = mapUidToMonthDict[u[0]].values()
        m1 = mapUidToMonthDict[u[1]].values()
        writer.writerow( (u[0], u[1], cross_entropy(d0, d1), pearsonr(d0, d1)[0], distance.euclidean(d0, d1), cross_entropy(h0, h1), pearsonr(h0, h1)[0], distance.euclidean(h0, h1), cross_entropy(m0, m1), pearsonr(m0, m1)[0], distance.euclidean(m0, m1)) )
        uniqueUser.add( (u[0], u[1]) )

        cnt += 1
        print cnt
f.close()
print "Finish"