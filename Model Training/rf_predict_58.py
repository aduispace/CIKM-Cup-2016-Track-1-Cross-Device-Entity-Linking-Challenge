
# coding: utf-8

# In[2]:

import pickle
import operator
from tqdm import tqdm
import numpy as np
from datetime import datetime
from sklearn.preprocessing import normalize
from sklearn.metrics import classification_report

feature_num = 58
thereshold = [0.50,0.51,0.52,0.53,0.54,0.55,0.56,0.57,0.58,0.59,0.60,0.61,0.62,0.63,0.64,0.65,0.66,0.67,0.68,0.69,0.70]
# thereshold = [0.70,0.71,0.72,0.73]

with open('./new_rf_classifier.pkl', 'rb') as fid:
    grd = pickle.load(fid)

#   load test features
test_data = {}
with open ('./Test_Features_58.pickle','rb') as f_in:
    test_data = pickle.load(f_in)
true_pair = []
with open('./Valid_Pair/valid.csv','r') as f_in:
    for line in tqdm(f_in):
        user1,user2 = line.strip().split(',')
        true_pair.append((user1,user2))
with open('./Valid_Pair/valid_2.csv','r') as f_in:
    for line in tqdm(f_in):
        user1,user2 = line.strip().split(',')
        true_pair.append((user1,user2))
true_pair = set(true_pair)
test_pair = sorted(list(test_data.keys()))
for i in tqdm(range(len(test_pair))):
    test_data[test_pair[i]][9] = float(test_data[test_pair[i]][9])/86400
    test_data[test_pair[i]][10] = float(test_data[test_pair[i]][10])/86400

cont = 0
for i in tqdm(range(len(test_pair))):
    if test_pair[i] in true_pair:
        cont += 1
print('Number of pairs in test data also in Valid pair = {}'.format(cont))

#   Transfer data to numpy array/Matrix
test_set_x = np.zeros( shape = (len(test_pair),feature_num ) )
print("Test Matrix x's Size = {}".format(test_set_x.shape))
# ##  Notice! we only have 18 features with values
# ##  we set the rest 540 to zeros
# for i in tqdm(range(len(test_pair))):
#     temp = list(map(float,test_data[test_pair[i]]))
#     for j in range(len(temp)):
#         test_set_x[i][j] = temp[j]

# use the following code for faster processing if we do not need to fill features
for i in tqdm(range(len(test_pair))):
    test_set_x[i] = list(map(float,test_data[test_pair[i]]))

del test_data
test_set_x[np.isnan(test_set_x)] = 0
test_data_x = normalize(test_set_x)
del test_set_x

## Calculate F1
y_predict = grd.predict_proba(test_data_x)
y_true = np.zeros(shape = (1,len(y_predict)))
temp_pair = {}
for i in tqdm(range(len(test_pair))):
    temp_pair[test_pair[i]] = y_predict[i][1]
sortedPair = sorted(temp_pair.items(), key = operator.itemgetter(1), reverse = True)


# In[9]:

ListTreshold = []
ListPrecision = []
ListRecall = []
ListF1Score = []

for t in thereshold:
    hand_in_num = 0
    for i in range(len(sortedPair)):
        if sortedPair[i][1] < t:
            break
        hand_in_num += 1
    y_true = []
    for i in range(hand_in_num):
        if sortedPair[i][0] in true_pair:
            y_true += [1]
        else:
            y_true += [0]
    cont_TP = 0.
    cont_FP = 0.
    cont_FN = 0.
    for i in y_true:
        if i == 1:
            cont_TP += 1
        else:
            cont_FP += 1
    cont_FN = len(true_pair) - cont_TP
    precision = cont_TP/(cont_TP+cont_FP)
    recall = cont_TP/(cont_TP+cont_FN)
    ListTreshold.append(t)
    ListPrecision.append(precision)
    ListRecall.append(recall)
    ListF1Score.append(2*precision*recall/(precision+recall))


# In[22]:

get_ipython().magic(u'matplotlib inline')
import matplotlib
import matplotlib.pyplot as plt
plt.figure(figsize = (30,10))
plt.subplot(1, 3, 1)
plt.title('Precision', fontsize = 25, color = '#9b596B')
plt.xlabel('Threshold', fontsize = 25)
plt.plot(ListTreshold, ListPrecision, color = '#9b596B')
plt.subplot(1, 3, 2)
plt.title('Recall', fontsize = 25, color = '#99CC01')
plt.xlabel('Threshold', fontsize = 25,)
plt.plot(ListTreshold, ListRecall, color = '#99CC01')
plt.subplot(1, 3, 3)
plt.title('F1 Score', fontsize = 25, color = '#0D8ECF')
plt.xlabel('Threshold', fontsize = 25,)
plt.plot(ListTreshold, ListF1Score, color = '#0D8ECF')
plt.show()





