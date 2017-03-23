from tqdm import tqdm
from datetime import datetime
import pickle

with open('/Users/jiangpei/Desktop/CS249_data/new_facts.pickle', 'rb') as handle:
    new_facts = pickle.load(handle)

#Loop through all users:
url_pairs1={}
pair_urls1={}
#i = 0
print(datetime.today().strftime("%m/%d %H:%M:%S 1start"))

with open('/Users/jiangpei/Desktop/CS249_data/random/xaa.csv','r') as f_in:
    for line in tqdm(f_in):
        #print(i)
        #i = i + 1

        matched_user = line.strip().split(',')

        usr1 = matched_user[0]
        usr2 = matched_user[1]
        pair = [usr1, usr2]

        url1 = new_facts[usr1]
        url2 = new_facts[usr2]

        #intersection: O(min(m,n))
        common_urls = url1&url2
        pair_urls1[(usr1,usr2)] = common_urls

        for m in common_urls:

            if m not in url_pairs1:
                url_pairs1[m] = 0

            url_pairs1[m] = url_pairs1[m] + 1
print (datetime.today().strftime("%m/%d %H:%M:%S 1Process finished"))


url_pairs2={}
pair_urls2={}
print(datetime.today().strftime("%m/%d %H:%M:%S 2start"))

with open('/Users/jiangpei/Desktop/CS249_data/random/xab.csv','r') as f_in:
    for line in tqdm(f_in):
        #print(i)
        #i = i + 1

        matched_user = line.strip().split(',')

        usr1 = matched_user[0]
        usr2 = matched_user[1]
        pair = [usr1, usr2]

        url1 = new_facts[usr1]
        url2 = new_facts[usr2]

        #intersection: O(min(m,n))
        common_urls = url1&url2
        pair_urls2[(usr1,usr2)] = common_urls

        for m in common_urls:

            if m not in url_pairs2:
                url_pairs2[m] = 0

            url_pairs2[m] = url_pairs2[m] + 1
print (datetime.today().strftime("%m/%d %H:%M:%S 2Process finished"))


with open('pair_urls1.pickle', 'wb') as handle:
    pickle.dump(pair_urls1, handle, protocol=pickle.HIGHEST_PROTOCOL)
with open('pair_urls2.pickle', 'wb') as handle:
    pickle.dump(pair_urls2, handle, protocol=pickle.HIGHEST_PROTOCOL)
    

print(datetime.today().strftime("%m/%d %H:%M:%S combine start"))
result1 = {}

for key in (url_pairs1.viewkeys() | url_pairs2.keys()):
    result1[key] = 0
    if key in url_pairs1: result1[key] = result1[key] + url_pairs1[key]
    if key in url_pairs2: result1[key] = result1[key] + url_pairs2[key]

del url_pairs1
del url_pairs2

print (datetime.today().strftime("%m/%d %H:%M:%S  Combine Process finished"))

with open('result1.pickle', 'wb') as handle:
    pickle.dump(result1, handle, protocol=pickle.HIGHEST_PROTOCOL)
    
############################################################################################################
############################################################################################################

url_pairs3={}
pair_urls3={}

print(datetime.today().strftime("%m/%d %H:%M:%S 3start"))

with open('/Users/jiangpei/Desktop/CS249_data/random/xac.csv','r') as f_in:
    for line in tqdm(f_in):
        #print(i)
        #i = i + 1

        matched_user = line.strip().split(',')

        usr1 = matched_user[0]
        usr2 = matched_user[1]
        pair = [usr1, usr2]

        url1 = new_facts[usr1]
        url2 = new_facts[usr2]

        #intersection: O(min(m,n))
        common_urls = url1&url2
        pair_urls3[(usr1,usr2)] = common_urls

        for m in common_urls:

            if m not in url_pairs3:
                url_pairs3[m] = 0

            url_pairs3[m] = url_pairs3[m] + 1
            
print (datetime.today().strftime("%m/%d %H:%M:%S 3Process finished"))

url_pairs4={}
pair_urls4={}

print(datetime.today().strftime("%m/%d %H:%M:%S 4start"))

with open('/Users/jiangpei/Desktop/CS249_data/random/xad.csv','r') as f_in:
    for line in tqdm(f_in):
        #print(i)
        #i = i + 1

        matched_user = line.strip().split(',')

        usr1 = matched_user[0]
        usr2 = matched_user[1]
        pair = [usr1, usr2]

        url1 = new_facts[usr1]
        url2 = new_facts[usr2]

        #intersection: O(min(m,n))
        common_urls = url1&url2
        pair_urls4[(usr1,usr2)] = common_urls

        for m in common_urls:

            if m not in url_pairs4:
                url_pairs4[m] = 0

            url_pairs4[m] = url_pairs4[m] + 1
print (datetime.today().strftime("%m/%d %H:%M:%S 4Process finished"))


with open('pair_urls3.pickle', 'wb') as handle:
    pickle.dump(pair_urls3, handle, protocol=pickle.HIGHEST_PROTOCOL)
with open('pair_urls4.pickle', 'wb') as handle:
    pickle.dump(pair_urls4, handle, protocol=pickle.HIGHEST_PROTOCOL)
    

print(datetime.today().strftime("%m/%d %H:%M:%S combine start"))

result2 = {}

for key in (url_pairs3.viewkeys() | url_pairs4.keys()):
    result2[key] = 0
    if key in url_pairs3: result2[key] = result2[key] + url_pairs3[key]
    if key in url_pairs4: result2[key] = result2[key] + url_pairs4[key]

del url_pairs3
del url_pairs4

print (datetime.today().strftime("%m/%d %H:%M:%S  Combine Process finished"))

with open('result2.pickle', 'wb') as handle:
    pickle.dump(result2, handle, protocol=pickle.HIGHEST_PROTOCOL)
    
############################################################################################################
############################################################################################################

url_pairs5={}
pair_urls5={}

print(datetime.today().strftime("%m/%d %H:%M:%S 5start"))

with open('/Users/jiangpei/Desktop/CS249_data/random/xae.csv','r') as f_in:
    for line in tqdm(f_in):
        #print(i)
        #i = i + 1

        matched_user = line.strip().split(',')

        usr1 = matched_user[0]
        usr2 = matched_user[1]
        pair = [usr1, usr2]

        url1 = new_facts[usr1]
        url2 = new_facts[usr2]

        #intersection: O(min(m,n))
        common_urls = url1&url2
        pair_urls5[(usr1,usr2)] = common_urls

        for m in common_urls:

            if m not in url_pairs5:
                url_pairs5[m] = 0

            url_pairs5[m] = url_pairs5[m] + 1
print (datetime.today().strftime("%m/%d %H:%M:%S 5Process finished"))
    
with open('result3.pickle', 'wb') as handle:
    pickle.dump(url_pairs5, handle, protocol=pickle.HIGHEST_PROTOCOL)


############################################################################################################
############################################################################################################

with open('result1.pickle', 'rb') as handle:
    result1 = pickle.load(handle)

with open('result2.pickle', 'rb') as handle:
    result2 = pickle.load(handle)

print(datetime.today().strftime("%m/%d %H:%M:%S combine start"))
result_12 = {}

for key in (result1.viewkeys() | result2.keys()):
    result_12[key] = 0
    if key in result1: result_12[key] = result_12[key] + result1[key]
    if key in result2: result_12[key] = result_12[key] + result2[key]

with open('result_12.pickle', 'wb') as handle:
    pickle.dump(result_12, handle, protocol=pickle.HIGHEST_PROTOCOL)

print (datetime.today().strftime("%m/%d %H:%M:%S  Combine Process finished"))

############################################################################################################
############################################################################################################

with open('result_12.pickle', 'rb') as handle:
    result_12 = pickle.load(handle)

with open('result3.pickle', 'rb') as handle:
    result3 = pickle.load(handle)

print(datetime.today().strftime("%m/%d %H:%M:%S combine start"))
result_all = {}

for key in (result_12.viewkeys() | result3.keys()):
    result_all[key] = 0
    if key in result_12: result_all[key] = result_all[key] + result_12[key]
    if key in result3: result_all[key] = result_all[key] + result3[key]

with open('result_all.pickle', 'wb') as handle:
    pickle.dump(result_all, handle, protocol=pickle.HIGHEST_PROTOCOL)

print (datetime.today().strftime("%m/%d %H:%M:%S  Combine Process finished"))




