import pickle
import operator
from tqdm import tqdm
import numpy as np
from datetime import datetime
from sklearn.preprocessing import normalize
from sklearn.metrics import classification_report

feature_num = 558
thereshold = [0.50,0.51,0.52,0.53,0.54,0.55,0.56,0.57,0.58,0.59,0.60,0.61,0.62,0.63,0.64,0.65,0.66,0.67,0.68,0.69,0.70]

## chenge classifier file name
with open('grd_classifier_58.pkl', 'rb') as fid:
    grd = pickle.load(fid, encoding='latin1')

# #   load test features 58
# test_data = {}
# with open ('Test_Features_58.pickle','rb') as f_in:
#     test_data = pickle.load(f_in)

# #   load test features 558
temp_data = {}
test_data = {}
with open ('Test_features_558/Test_Features_1.pickle','rb') as f_in:
    temp_data = pickle.load(f_in)
test_data.update(temp_data)
with open ('Test_features_558/Test_Features_2.pickle','rb') as f_in:
    temp_data = pickle.load(f_in)
test_data.update(temp_data)
with open ('Test_features_558/Test_Features_3.pickle','rb') as f_in:
    temp_data = pickle.load(f_in)
test_data.update(temp_data)
with open ('Test_features_558/Test_Features_4.pickle','rb') as f_in:
    temp_data = pickle.load(f_in)
test_data.update(temp_data)
with open ('Test_features_558/Test_Features_5.pickle','rb') as f_in:
    temp_data = pickle.load(f_in)
test_data.update(temp_data)


true_pair = []
with open('Valid_Pair/valid.csv','r') as f_in:
    for line in tqdm(f_in):
        user1,user2 = line.strip().split(',')
        true_pair.append((user1,user2))
with open('Valid_Pair/valid_2.csv','r') as f_in:
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
    cont_TP = 0
    cont_FP = 0
    cont_FN = 0
    for i in y_true:
        if i == 1:
            cont_TP += 1
        else:
            cont_FP += 1
    cont_FN = len(true_pair) - cont_TP
    precision = cont_TP/(cont_TP+cont_FP)
    recall = cont_TP/(cont_TP+cont_FN)
    print('Threshold = {}'.format(t))
    print('Precision = {}'.format(precision))
    print('Recall = {}'.format(recall))
    print('F1 Score = {}'.format(2*precision*recall/(precision+recall)))

##  predict class with probability
##  test classifier
# ROC = {}
# y_predict = grd.predict_proba(test_data_x)
# y_true = np.zeros(shape = (1,len(y_predict)))
# for t in thereshold:
#     cont_TP = 0
#     cont_PredictP = 0
#     cont_P = 0
#     for i in range(len(y_predict)):
#         if y_predict[i][1]>t:
#             cont_PredictP += 1
#             if (test_pair[i] in true_pair):
#                 cont_TP += 1
#         if (test_pair[i] in true_pair):
#             cont_P += 1
#             y_true[0][i] = 1
#         else:
#             y_true[0][i] = 0
#     print('Thereshold of pridiction = {}'.format(t))
#     print('True positive rate = {}'.format(cont_TP/cont_P))
#     print('False positive rate = {}'.format((cont_PredictP-cont_TP)/(len(y_predict)-cont_P)))
#     print(classification_report(y_true, y_predict))
#     # print('cont_TP = {}'.format(cont_TP))
#     # print('cont_PredictP = {}'.format(cont_PredictP))
#     # print('cont_P = {}'.format(cont_P))

##  predict class with lable
# y_predict = grd.predict(test_data_x)
# cont = 0
# for i in tqdm(range(len(y_predict))):
#     if y_predict[i]==1 and (test_pair[i] in true_pair):
#         cont += 1
# print('Number of pairs that are pridicted to be 1 and it is valid = {}'.format(cont))
