import json
import pytz
import numpy as np
from tqdm import tqdm   # install tqdm package(a progress meter) by
                        # enter 'pip install tqdm' in terminal

from datetime import datetime
from sklearn.feature_extraction.text import TfidfVectorizer

## Insert an item at a given position. The first argument is the index of the element before which to insert, so a.insert(0, x) inserts at the front of the list, and a.insert(len(a), x) is equivalent to a.append(x) .

print(datetime.today().strftime("%m/%d %H:%M:%S start"))

##  File: facts.csv
#   facts[uid] is a list!!!
facts = {}
counter = 0
with open('C:/Users/lindu/Desktop/Winter 2017 Classes/CS249/Project/Code/data-train-dca/facts.json') as f_in:
    for line in tqdm(f_in): # a uid a line
    #  for i in range(100):
    #     line=f_in.readline()

        j = json.loads(line.strip())
        if j.get('uid') not in facts:
            facts[j.get('uid')]=[]
            overlap_list = [] # a list to store all times
        for x in j.get('facts'): # ‘facts’ is a list of dict, so it can be iterated, x是每一个dict!!!
           # ts = x['ts'] / 1000 # 10-digits is valid
            if (len(str(x['ts'])) == 13):
               date = datetime.fromtimestamp(x['ts'] / 1000, pytz.utc).strftime('%m-%d')
               overlap_list.insert(0, date)
        counter = counter + 1
        facts[j.get('uid')] = overlap_list


##  Create facts file based on File: train.csv
#   users_for_predict contains userid not in the given File: train.csv
with open('OverLapDay_ToBeTrained.txt','w') as f_out: # output facts.txt
    with open('C:/Users/lindu/Desktop/Winter 2017 Classes/CS249/Project/Code/data-train-dca/Train_features.txt') as f_in:
        for line in tqdm(f_in):
            part = line.strip().split('\t')
            user1 = part[0]
            user2 = part[1]
            overlap_set = set(facts[user1]) & set(facts[user2]) # use a new set to calculate # of common elements
            nums = len(overlap_set)
            t = str(user1) + ',' + str(user2) + ',' + str(nums)
            f_out.write(t+'\n')
