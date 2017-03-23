import json
import numpy as np
import sys
from tqdm import tqdm   # install tqdm package(a progress meter) by
                        # enter 'pip install tqdm' in terminal
from datetime import datetime
from sklearn.feature_extraction.text import TfidfVectorizer

print(datetime.today().strftime("%m/%d %H:%M:%S start"))
"""
unique_user = set()
with open('data-train-dca/train.csv','r') as f_in:
    for line in tqdm(f_in):
        matched_user = line.strip().split(',')
        unique_user.add(matched_user[0])
        unique_user.add(matched_user[1])

      
#pruning facts        
new_facts = {}
for key in facts:
    if key in unique_user:
        new_facts[key]=set(facts[key])
"""
import pickle
with open('/Users/YangG/Desktop/249proj/Code/sorted_ratioLift.pickle', 'rb') as handle:
    sorted_rl= pickle.load(handle)

buckets=[]
url_bucket={}
for i in range(40):#5->40
    tmp=[]
    for j in range(100*i,100*i+100):### 2->100 
        tmp.append(sorted_rl[j][0])
        url_bucket[sorted_rl[j][0]]=i
    buckets.append(tmp)

top500={}
for i in range(5):#5->40
    for j in range(100): #2->100
        top500[buckets[i][j]]=i*100+j
        
#KeyURLDist&TopURLHit
with open('/Users/YangG/Desktop/249proj/Code/pair_common_urls_testing.pickle', 'rb') as handle:
    pair_urls= pickle.load(handle)

keyURLDist={}
topURLHit={}
for key in pair_urls:
    counter=[0]*40
    hit=[0]*500
    for url in pair_urls[key]:
        if url in url_bucket:
            counter[url_bucket[url]]=counter[url_bucket[url]]+1
        if url in top500:
            hit[top500[url]]=1
    keyURLDist[key]=counter
    topURLHit[key]=hit

with open('test_keyURLDist.pickle', 'wb') as handle:
    pickle.dump(keyURLDist, handle, protocol=pickle.HIGHEST_PROTOCOL)
topURLHit_1=dict(list(topURLHit.items())[0:1200000])
with open('test_topURLHit1.pickle', 'wb') as handle:
    pickle.dump(topURLHit_1, handle, protocol=pickle.HIGHEST_PROTOCOL)
topURLHit_2=dict(list(topURLHit.items())[1200000:])
with open('test_topURLHit2.pickle', 'wb') as handle:
    pickle.dump(topURLHit_2, handle, protocol=pickle.HIGHEST_PROTOCOL)
