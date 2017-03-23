import json
import numpy as np
import sys
from tqdm import tqdm   # install tqdm package(a progress meter) by
                        # enter 'pip install tqdm' in terminal
from datetime import datetime
from sklearn.feature_extraction.text import TfidfVectorizer

print(datetime.today().strftime("%m/%d %H:%M:%S start"))

positive_list = {}
negative_list = []
cont_pair = 0
with open('data-train-dca/train.csv','r') as f_in:
    for line in tqdm(f_in):
        user1,user2 = line.strip().split(',')
        if user1 not in positive_list:
            positive_list[user1] = []
        if user2 not in positive_list:
            positive_list[user2] = []
        positive_list[user1] += [user2]
        positive_list[user2] += [user1]
unique_user_list = list(positive_list.keys())
temp_list = list(positive_list.keys())


with open('negative_list.csv','w') as f_out:
    for i in tqdm(range(len(unique_user_list))):
        if len(temp_list) <= 10000:
            break
        cont = 0
        negative_list = positive_list[unique_user_list[i]]
        while cont<=100:
            p = int(np.random.uniform(0,1)*len(temp_list))
            user = temp_list[p]
            if (user not in negative_list) and (user != unique_user_list[i]):
                f_out.write('%s,%s\n' % (unique_user_list[i],user))
                negative_list += [user]
                cont_pair += 1
                positive_list[user] += [unique_user_list[i]]
            cont += 1
        temp_list.remove(unique_user_list[i])

print('Negative Pairs = {}'.format(cont_pair))
