#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon Mar  6 21:02:30 2017

@author: jiangpei
"""

import json
from tqdm import tqdm
from datetime import datetime

unique_user = set()
with open('/Users/jiangpei/Desktop/CS249_data/data-train-dca/train.csv','r') as f_in:
    for line in tqdm(f_in):
        matched_user = line.strip().split(',')
        unique_user.add(matched_user[0])
        unique_user.add(matched_user[1])

#########################################################################################################
urls_tokens = {}
with open('/Users/jiangpei/Desktop/CS249_data/data-train-dca/urls.csv','r') as f_in:
    for line in tqdm(f_in):
    # for i in range(100):
    #     line=f_in.readline()
        key, tokens = line.strip().split(',')
        data = tokens.split('/')[0].split('?')
        if key not in urls_tokens:
            urls_tokens[key] = data # Only the first token
        else:
            urls_tokens[key] = urls_tokens[key]+data

facts = {}
with open('/Users/jiangpei/Desktop/CS249_data/data-train-dca/facts.json') as f_in:
    for line in tqdm(f_in):
    #  for i in range(100):
    #     line=f_in.readline()
        j = json.loads(line.strip())
        if j.get('uid') not in facts:
            facts[j.get('uid')]=[]
        for x in j.get('facts'):
            facts[j.get('uid')] += urls_tokens[str(x['fid'])]
#########################################################################################################                  

del urls_tokens
del matched_user
del line

#########################################################################################################            

#pruning facts        
new_facts = {}
for key in facts:
    if key in unique_user:
        new_facts[key] = set(facts[key])
        
#Loop through all users:
url_pairs={}
pair_urls={}
usr_list=list(new_facts.keys())

print(datetime.today().strftime("%m/%d %H:%M:%S start"))

for i in range(len(usr_list)):
    print(i)
    usr1=usr_list[i]
    url1=new_facts[usr1]
    for j in range(i+1,len(usr_list)):
        usr2=usr_list[j]
        url2=new_facts[usr2]
        pair=[usr1,usr2]
        #intersection: O(min(m,n))
        common_urls=url1&url2
        pair_urls[(usr1,usr2)]=common_urls
        for m in common_urls:
            if m not in url_pairs:
                url_pairs[m]=[]
            url_pairs[m].append(pair) 
                
print (datetime.today().strftime("%m/%d %H:%M:%S Process finished"))

with open('new_facts.pickle', 'wb') as fid:
    pickle.dump(new_facts, fid)
#########################################################################################################

#new_facts = {}
#for key, value in facts.iteritems():
#    if(key in unique_user):
#        new_facts[key] = value
#
#del value
#
#new_facts_key = new_facts.keys()
#pair = []
#url_pair = {}
#pair_list = []
#index_url = {}
#
#for i in range(0, len(new_facts_key)):
#    for j in range(i + 1, len(new_facts_key)):
#        pair.append(new_facts_key[i])
#        pair.append(new_facts_key[j])
#        
#        value1 = new_facts[new_facts_key[i]]
#        value2 = new_facts[new_facts_key[j]]
#         
#        common_url = [val for val in value1 if val in value2]
#        
#        for u in common_url:
#            if not u in url_pair.keys():
#                url_pair[u] = pair
#            else:
#                url_pair[u].append(pair)
#
#                
#
#    
#url_pair = {}
#user_pair = set()
        

#########################################################################################################
                
                
                
                