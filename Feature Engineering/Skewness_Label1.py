import json
import numpy as np
from tqdm import tqdm   # install tqdm package(a progress meter) by
                        # enter 'pip install tqdm' in terminal

from datetime import datetime, timedelta
from sklearn.feature_extraction.text import TfidfVectorizer

## Insert an item at a given position. The first argument is the index of the element before which to insert, so a.insert(0, x) inserts at the front of the list, and a.insert(len(a), x) is equivalent to a.append(x) .

print(datetime.today().strftime("%m/%d %H:%M:%S start"))

##  File: facts.csv
#   facts[uid] is a list!!!
facts = {}
with open('C:/Users/lindu/Desktop/Winter 2017 Classes/CS249/Project/Code/data-train-dca/facts.json') as f_in:
    for line in tqdm(f_in): # a uid a line
    #  for i in range(100):
    #     line=f_in.readline()
        j = json.loads(line.strip())
        if j.get('uid') not in facts:
            facts[j.get('uid')]=[]
        time_list = [] # a list to store all times
        for x in j.get('facts'): # ‘facts’ is a list of dict, so it can be iterated, x是每一个dict!!!
            time_list.insert(0, x['ts'])
        time_list.sort()
        minmaxtime = [time_list[0], time_list[-1]] # -1 is the last element
        facts[j.get('uid')] = minmaxtime # fact {uid: [min time, max time],.. : ....}

##  Create facts file based on File: train.csv
#   users_for_predict contains userid not in the given File: train.csv
users_in_train = set()
with open('Skewness.txt','w') as f_out: # output facts.txt
    with open('C:/Users/lindu/Desktop/Winter 2017 Classes/CS249/Project/Code/data-train-dca/train.csv') as f_in:
        for line in tqdm(f_in):
            user1,user2 = line.strip().split(',')
            lifespan1 = (facts[user1])[1] - (facts[user1])[0]
            lifespan2 = (facts[user2])[1] - (facts[user2])[0]
            skewness = min(lifespan1, lifespan2) / max(lifespan1, lifespan2)
            t = str(user1) + ',' + str(user2) + ',' + str(skewness)
            f_out.write(t+'\n')
#             users_in_train.update([user1,user2])
# users_for_predict = set(facts.keys()).difference(users_in_train)

# ##  Create facts_test file based on File: train.csv
# users_for_predict_list = sorted(list(users_for_predict))
# with open('facts_test.tsv','w') as f_out:
#     for x in users_for_predict_list:
#         t = str(facts[x]).replace("'",'').replace("[",' ').replace("]",' ').replace(' ','')
#         f_out.write("%s\t%s\n" % (x,t)) # printout string

# del users_for_predict_list
# del users_in_train
# del users_for_predict

# print (datetime.today().strftime("%m/%d %H:%M:%S Process finished"))

# ##  TF-IDF matrix on user’s domains
