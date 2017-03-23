#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar 13 23:52:47 2017

@author: YangG
"""
reduced_features_train={}
with open('/Users/YangG/Desktop/249proj/Code/DayCE.csv', 'r') as f1, open('/Users/YangG/Desktop/249proj/Code/DayCor.csv', 'r') as f2, open('/Users/YangG/Desktop/249proj/Code/DayTemporalDist.csv', 'r') as f3,open('/Users/YangG/Desktop/249proj/Code/HourCE.csv', 'r') as f4,open('/Users/YangG/Desktop/249proj/Code/HourCor.csv', 'r') as f5,open('/Users/YangG/Desktop/249proj/Code/HourTemporalDist.csv', 'r') as f6,open('/Users/YangG/Desktop/249proj/Code/MonthCE.csv', 'r')as f7,open('/Users/YangG/Desktop/249proj/Code/MonthCor.csv', 'r') as f8,open('/Users/YangG/Desktop/249proj/Code/MonthTemporalDist.csv', 'r') as f9:
    for l1,l2,l3,l4,l5,l6,l7,l8,l9 in zip(f1,f2,f3,f4,f5,f6,f7,f8,f9):
        user1,user2,ft1=l1.strip().split(',')
        ft2=l2.strip().split(',')[2]
        ft3=l3.strip().split(',')[2]
        ft4=l4.strip().split(',')[2]
        ft5=l5.strip().split(',')[2]
        ft6=l6.strip().split(',')[2]
        ft7=l7.strip().split(',')[2]
        ft8=l8.strip().split(',')[2]
        ft9=l9.strip().split(',')[2]
        reduced_features_train[(user1,user2)]=[ft1,ft2,ft3,ft4,ft5,ft6,ft7,ft8,ft9]
print(len(reduced_features_train))
                             
with open('/Users/YangG/Desktop/249proj/Code/FirstDate_ToBeTrained.txt', 'r') as f1, open('/Users/YangG/Desktop/249proj/Code/LastDate_ToBeTrained.txt', 'r') as f2, open('/Users/YangG/Desktop/249proj/Code/OverLapDay_ToBeTrained.txt', 'r') as f3,open('/Users/YangG/Desktop/249proj/Code/Skewness_ToBeTrained.txt', 'r') as f4:
    for line1, line2,line3,line4 in zip(f1, f2,f3,f4):
        user1=line1.strip().split(',')[0]
        user2=line1.strip().split(',')[1]
        ft1=line1.strip().split(',')[2]
        ft2=line2.strip().split(',')[2]
        ft3=line3.strip().split(',')[2]
        ft4=line4.strip().split(',')[2]
        reduced_features_train[(user1,user2)]+=[ft1,ft2,ft3,ft4]
print(len(reduced_features_train))

from tqdm import tqdm
with open('/Users/YangG/Desktop/249proj/Code/Train_features.txt','r') as f_in:
    for line in tqdm(f_in):
        user1=line.strip().split('\t')[0]
        user2=line.strip().split('\t')[1]
        feature_list=line.strip().split('\t')[2:]
        reduced_features_train[(user1,user2)]+=feature_list
print(len(reduced_features_train))

train_keys=list(reduced_features_train.keys())

import pickle
with open('reduced_keyURLDist.pickle', 'rb') as handle:
    reduced_keyURLDist=pickle.load(handle)
for key in tqdm(train_keys):
    reduced_features_train[key]+=reduced_keyURLDist[key]
del reduced_keyURLDist
del train_keys  
  
with open('reduced_topURLHit1.pickle', 'rb') as handle:
    reduced_topURLHit=pickle.load(handle)
train_keys=list(reduced_topURLHit.keys())
for key in tqdm(train_keys):
    reduced_features_train[key]+=reduced_topURLHit[key]
del reduced_topURLHit
del train_keys  
    
with open('reduced_topURLHit2.pickle', 'rb') as handle:
    reduced_topURLHit=pickle.load(handle)   
train_keys=list(reduced_topURLHit.keys())
for key in tqdm(train_keys):
    reduced_features_train[key]+=reduced_topURLHit[key]
del reduced_topURLHit
del train_keys  

reduced_features_train1=dict(list(reduced_features_train.items())[0:563833])
with open('Reduced_Features_train1.pickle', 'wb') as handle:
    pickle.dump(reduced_features_train1, handle, protocol=pickle.HIGHEST_PROTOCOL)
del reduced_features_train1

reduced_features_train2=dict(list(reduced_features_train.items())[563833:1127666])
with open('Reduced_Features_train2.pickle', 'wb') as handle:
    pickle.dump(reduced_features_train2, handle, protocol=pickle.HIGHEST_PROTOCOL)
del reduced_features_train2

reduced_features_train3=dict(list(reduced_features_train.items())[1127666:1691499])
with open('Reduced_Features_train3.pickle', 'wb') as handle:
    pickle.dump(reduced_features_train3, handle, protocol=pickle.HIGHEST_PROTOCOL)
del reduced_features_train3

reduced_features_train4=dict(list(reduced_features_train.items())[1691499:2255332])
with open('Reduced_Features_train4.pickle', 'wb') as handle:
    pickle.dump(reduced_features_train4, handle, protocol=pickle.HIGHEST_PROTOCOL)
del reduced_features_train4

reduced_features_train5=dict(list(reduced_features_train.items())[2255332:])
with open('Reduced_Features_train5.pickle', 'wb') as handle:
    pickle.dump(reduced_features_train5, handle, protocol=pickle.HIGHEST_PROTOCOL)
del reduced_features_train5

"""
#For check
import pickle
with open('Reduced_features/Reduced_Features_train5.pickle', 'rb') as handle:
    chunk=pickle.load(handle)
with open('Features_train5.pickle','wb') as handle:    
    pickle.dump(chunk, handle, protocol=2)
del chunk   

print(len(chunk))
print(len(list(chunk.values())[0]))
key=list(chunk.keys())[0]
print(chunk[key])
check5=dict(list(chunk.items())[0:100])
""