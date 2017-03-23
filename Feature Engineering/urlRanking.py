from datetime import datetime
import pickle

#numerator
print(datetime.today().strftime("%m/%d %H:%M:%S numerator start"))

with open('/Users/jiangpei/Desktop/CS249_data/url_pairs_matched.pickle', 'rb') as handle:
    url_pairs_matched = pickle.load(handle)

num_matched_pair = 506136.0

url_ratio_matched = {}

for k in url_pairs_matched.keys():
#    print(len(url_pairs_matched[k])/num_matched_pair)
    url_ratio_matched[k] = len(url_pairs_matched[k])/num_matched_pair

print (datetime.today().strftime("%m/%d %H:%M:%S numerator Process finished"))

############################################################################################################
############################################################################################################

#denominator
print(datetime.today().strftime("%m/%d %H:%M:%S denominator start"))

num_random_pair = 23287009.0

url_ratio_random = {}

for k in result_all.keys():
#    print(len(url_pairs_random[k])/num_random_pair)
    url_ratio_random[k] = result_all[k]/num_random_pair

print (datetime.today().strftime("%m/%d %H:%M:%S denominator Process finished"))

#ratioLift
print(datetime.today().strftime("%m/%d %H:%M:%S ratioLift start"))

url_part1 = url_ratio_matched.keys()
url_part2 = url_ratio_random.keys()
url_rationLift = {}

for u in url_part2:
    if(u in url_part1):
        url_rationLift[u] = url_ratio_matched[u]/url_ratio_random[u]
    else:
        url_rationLift[u] = 0

print (datetime.today().strftime("%m/%d %H:%M:%S ratioLift Process finished"))

with open('url_rationLift.pickle', 'wb') as handle:
    pickle.dump(url_rationLift, handle, protocol=pickle.HIGHEST_PROTOCOL)

import operator
sorted_ratioLift = sorted(url_rationLift.items(), key=operator.itemgetter(1))
sorted_ratioLift = list(reversed(sorted_ratioLift))

with open('sorted_ratioLift.pickle', 'wb') as handle:
    pickle.dump(sorted_ratioLift, handle, protocol=pickle.HIGHEST_PROTOCOL)
