### Read training data from file
import pickle
from tqdm import tqdm
import numpy as np
from datetime import datetime
from sklearn.preprocessing import normalize

##  Load data
train_data = {}
with open ('Reduced_features/Reduced_Features_train1.pickle','rb') as f_in:
    temp_train = pickle.load(f_in)
train_data.update(temp_train)
with open ('Reduced_features/Reduced_Features_train2.pickle','rb') as f_in:
    temp_train = pickle.load(f_in)
train_data.update(temp_train)
with open ('Reduced_features/Reduced_Features_train3.pickle','rb') as f_in:
    temp_train = pickle.load(f_in)
train_data.update(temp_train)
with open ('Reduced_features/Reduced_Features_train4.pickle','rb') as f_in:
    temp_train = pickle.load(f_in)
train_data.update(temp_train)
with open ('Reduced_features/Reduced_Features_train5.pickle','rb') as f_in:
    temp_train = pickle.load(f_in)
train_data.update(temp_train)
#   Transfer DateGap from second to minute
train_pair = sorted(list(train_data.keys()))
for i in tqdm(range(len(train_pair))):
    train_data[train_pair[i]][9] = float(train_data[train_pair[i]][9])/86400
    train_data[train_pair[i]][10] = float(train_data[train_pair[i]][10])/86400
##  Create training set
#   Positive pair list
#   [u1,u2]
temp = []
with open('data-train-dca/train.csv','r') as f_in:
    for line in f_in:
        user1,user2 = line.strip().split(',')
        temp.append((user1,user2))
positive_pair = set(temp) # some positive pairs do not contain html information
                          # but we don't need to consider this situatioin
                          # because our training pairs aleady eliminate those pairs
del temp
#   Transfer data to numpy array/Matrix
train_set_x = np.zeros( shape = (len(train_pair),len(train_data[train_pair[0]])) )
train_data_y = np.zeros( shape = (len(train_pair),1) )
print("Train Matrix x's Size = {}".format(train_set_x.shape))
print("Train Matrix y's Size = {}".format(train_data_y .shape))
for i in tqdm(range(len(train_pair))):
    train_set_x[i] = list(map(float,train_data[train_pair[i]]))
    if train_pair[i] in positive_pair:
        train_data_y[i] = 1
    else:
        train_data_y[i] = 0
del train_data
train_set_x[np.isnan(train_set_x)] = 0
train_data_x = normalize(train_set_x)
del train_set_x

### Train Classifier

from sklearn.ensemble import (RandomForestClassifier,GradientBoostingClassifier)
from sklearn.svm import SVC
from sklearn.preprocessing import normalize

grd = GradientBoostingClassifier(loss='deviance', learning_rate=0.1, n_estimators=10,verbose = 1)
# rf = RandomForestClassifier(max_depth=3, n_estimators=100, verbose = 1)
# svm = SVC(C = 1.0, verbose = True) # kernel = ‘rbf’/(‘linear’, ‘poly’, ‘sigmoid’),gamma =

print(datetime.today().strftime("%m/%d %H:%M:%S grd start"))
grd.fit(train_data_x,train_data_y.ravel())
print(datetime.today().strftime("%m/%d %H:%M:%S grd end"))

# save the classifier
with open('grd_classifier_558.pkl', 'wb') as fid:
    pickle.dump(grd, fid)
