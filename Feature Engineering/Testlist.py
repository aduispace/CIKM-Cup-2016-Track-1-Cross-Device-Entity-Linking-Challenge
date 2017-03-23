#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar 16 22:32:50 2017

@author: YangG
"""

from tqdm import tqdm   # install tqdm package(a progress meter) by
                        # enter 'pip install tqdm' in terminal
from sklearn.feature_extraction.text import TfidfVectorizer

#TF-IDF
print ("Tfidf for urls Starts.")
users_test, row_text = {},[]
URL_tf_test = TfidfVectorizer(min_df=2, lowercase=False, sublinear_tf =True).fit(
map(lambda x: x.strip().split('\t')[-1],open('facts_test.tsv','r').readlines()))
print ("Size Vobab on URL_tf_test = {}".format(len(URL_tf_test.idf_)))
row_num = 0
with open('facts_test.tsv','r') as f_in:
    for line in tqdm(f_in):
        user, t = line.strip().split('\t')
        users_test[user] = row_num
        row_num += 1
        row_text.append(t)
URL_dt_test = URL_tf_test.transform(row_text)
print ("Document-term matrix on URL_test = {}".format(URL_dt_test.shape))

#KNN neighbours
from sklearn.neighbors import KNeighborsClassifier

knn = KNeighborsClassifier(n_neighbors=1)
knn.fit(URL_dt_test, range(1, URL_dt_test.shape[0] + 1))
users=list(users_test.keys())
def get_predict(line):
    res = []
    user_id, tokens = line.strip().split('\t')
    tmp = knn.kneighbors(X=URL_tf_test.transform([tokens]), n_neighbors=30, return_distance=True)
    for i in range(len(tmp[0][0])):
        if user_id < users[tmp[1][0][i]]:
            res.append((user_id, users[tmp[1][0][i]], tmp[0][0][i]))
        else:
            res.append((users[tmp[1][0][i]], user_id, tmp[0][0][i]))
    return res

#get test pairs
results=[]
with open('facts_test.tsv','r') as f_in:
    for line in tqdm(f_in):
        results.append(get_predict(line))
#write results
import pickle
with open('knnlist.pickle','wb') as handle:
    pickle.dump(results,handle,protocol=2)

