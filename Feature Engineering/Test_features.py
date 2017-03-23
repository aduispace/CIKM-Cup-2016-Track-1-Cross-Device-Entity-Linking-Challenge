
# coding: utf-8

# In[1]:

from tqdm import tqdm
test_features={}


# In[2]:

#Zhuang
with open('/Users/YangG/Desktop/249proj/Code/DayHourMonth.csv', 'r') as f1:
    for line1 in tqdm(f1):
        user1,user2,ft1,ft2,ft3,ft4,ft5,ft6,ft7,ft8,ft9=line1.strip().split(',')
        if user1==user2:
            continue
        test_features[(user1,user2)]=[ft1,ft2,ft3,ft4,ft5,ft6,ft7,ft8,ft9]
print(len(test_features))


# In[3]:

#Lin
with open('/Users/YangG/Desktop/249proj/Code/TestList_Feature.txt', 'r') as f1:
    for line1 in tqdm(f1):
        user1,user2,ft1,ft2,ft3,ft4=line1.strip().split(',')
        if user1==user2:
            continue
        if len(test_features[(user1,user2)])==13:
            continue
        test_features[(user1,user2)]+=[ft1,ft2,ft3,ft4]
        if len(test_features[(user1,user2)])>13:
            print((user1,user2))
            break
print(len(test_features))



# In[4]:

#Zeng
with open('/Users/YangG/Desktop/249proj/Code/Zeng/Test_features.txt','r') as f_in:
    for line in tqdm(f_in):
        user1=line.strip().split('\t')[0]
        user2=line.strip().split('\t')[1]
        if user1==user2:
            continue
        if len(test_features[(user1,user2)])==18:
            continue
        feature_list=line.strip().split('\t')[2:]
        test_features[(user1,user2)]+=feature_list
        if len(test_features[(user1,user2)])>18:
            print((user1,user2))
            break
print(len(test_features))



# In[6]:

#Guo
test_keys=list(test_features.keys())
import pickle
with open('/Users/YangG/test_keyURLDist.pickle', 'rb') as handle:
    test_keyURLDist=pickle.load(handle)
for key in tqdm(test_keys):
    if key[0]==key[1]:
        continue
    if len(test_features[key])==58:
            continue
    test_features[key]+=test_keyURLDist[key]
    if len(test_features[key])>58:
            print((user1,user2))
            break
del test_keyURLDist
del test_keys  
  


# In[7]:

with open('/Users/YangG/test_topURLHit1.pickle', 'rb') as handle:
    test_topURLHit=pickle.load(handle)
test_keys=list(test_topURLHit.keys())
for key in tqdm(test_keys):
    if key[0]==key[1]:
        continue
    if len(test_features[key])==558:
            continue
    test_features[key]+=test_topURLHit[key]
    if len(test_features[key])>558:
            print((user1,user2))
            break
del test_topURLHit
del test_keys  


# In[8]:

with open('/Users/YangG/test_topURLHit2.pickle', 'rb') as handle:
    test_topURLHit=pickle.load(handle)
test_keys=list(test_topURLHit.keys())
for key in tqdm(test_keys):
    if key[0]==key[1]:
        continue
    if len(test_features[key])==558:
            continue
    test_features[key]+=test_topURLHit[key]
    if len(test_features[key])>558:
            print((user1,user2))
            break
del test_topURLHit
del test_keys  


# In[ ]:

#check the length
"""
test_keys=list(test_features.keys())
for key in tqdm(test_keys):
    if len(test_features[key])!=558:
        print((user1,user2))
        break

"""
# In[ ]:

#Write out features
test_features_1=dict(list(test_features.items())[0:489389])

with open('Test_Features_1.pickle', 'wb') as handle:
    pickle.dump(test_features_1, handle, protocol=pickle.HIGHEST_PROTOCOL)
del test_features_1


# In[ ]:

test_features_2=dict(list(test_features.items())[489389:978777])
with open('Test_Features_2.pickle', 'wb') as handle:
    pickle.dump(test_features_2, handle, protocol=pickle.HIGHEST_PROTOCOL)
del test_features_2

test_features_3=dict(list(test_features.items())[978777:1468165])
with open('Test_Features_3.pickle', 'wb') as handle:
    pickle.dump(test_features_3, handle, protocol=pickle.HIGHEST_PROTOCOL)
del test_features_3

test_features_4=dict(list(test_features.items())[1468165:1957553])
with open('Test_Features_4.pickle', 'wb') as handle:
    pickle.dump(test_features_4, handle, protocol=pickle.HIGHEST_PROTOCOL)
del test_features_4

test_features_5=dict(list(test_features.items())[1957553:])
with open('Test_Features_5.pickle', 'wb') as handle:
    pickle.dump(test_features_5, handle, protocol=pickle.HIGHEST_PROTOCOL)
del test_features_5 


# In[ ]:
with open('Test_Features_58.pickle', 'wb') as handle:
    pickle.dump(test_features, handle, protocol=2)

