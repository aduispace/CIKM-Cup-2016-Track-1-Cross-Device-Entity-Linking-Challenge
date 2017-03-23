pfrom tqdm import tqdm
from datetime import datetime
import pickle

with open('new_facts.pickle', 'rb') as handle:
    new_facts = pickle.load(handle)

#Loop through all users:
url_pairs={}
pair_urls={}
i = 0
print(datetime.today().strftime("%m/%d %H:%M:%S start"))

with open('/Users/jiangpei/Desktop/CS249_data/data-train-dca/train.csv','r') as f_in:
    for line in tqdm(f_in):
        print(i)
        i = i + 1

        matched_user = line.strip().split(',')

        usr1 = matched_user[0]
        usr2 = matched_user[1]
        pair = [usr1, usr2]

        url1 = new_facts[usr1]
        url2 = new_facts[usr2]

        #intersection: O(min(m,n))
        common_urls = url1&url2
        pair_urls[(usr1,usr2)] = common_urls

        for m in common_urls:

            if m not in url_pairs:
                url_pairs[m] = []

            url_pairs[m].append(pair)

print (datetime.today().strftime("%m/%d %H:%M:%S Process finished"))

with open('url_pairs_matched.pickle', 'wb') as handle:
    pickle.dump(url_pairs, handle, protocol=pickle.HIGHEST_PROTOCOL)
with open('pair_urls_matched.pickle', 'wb') as handle:
    pickle.dump(pair_urls, handle, protocol=pickle.HIGHEST_PROTOCOL)