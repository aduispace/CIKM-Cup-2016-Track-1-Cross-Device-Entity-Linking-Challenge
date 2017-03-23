import json
import numpy as np
import sys
from tqdm import tqdm   # install tqdm package(a progress meter) by
                        # enter 'pip install tqdm' in terminal
from datetime import datetime
from sklearn.feature_extraction.text import TfidfVectorizer

print(datetime.today().strftime("%m/%d %H:%M:%S start"))

##  File: urls.csv
#   urls_tokens: [fid[urls],...] Only take 1 levle urls
urls_tokens = {}
with open('data-train-dca/urls.csv','r') as f_in:
    for line in tqdm(f_in):
    # for i in range(100):
    #     line=f_in.readline()
        key, tokens = line.strip().split(',')
        data = tokens.split('/')[0].split('?')
        if key not in urls_tokens:
            urls_tokens[key] = data # Only the first token
        else:
            urls_tokens[key] = urls_tokens[key]+data
#   html_titles: fid[title1,title2,...],...]
html_titles = {}
with open('data-train-dca/titles.csv','r') as f_in:
    for line in tqdm(f_in):
        key, tokens = line.strip().split(',')
        html_titles[key] = tokens.replace(' ',',')
##  File: facts.csv
#   connect uid to url/fid/html
facts = {}   # [uid[url,...],...]
facts_fid = {}   # [uid[fid,...],...]
facts_html = {}   # [uid[html,...],...]
with open('data-train-dca/facts.json','r') as f_in:
    for line in tqdm(f_in):
    #  for i in range(100):
    #     line=f_in.readline()
        j = json.loads(line.strip())
        if j.get('uid') not in facts:
            facts[j.get('uid')]=[]
            facts_html[j.get('uid')]=[]
            facts_fid[j.get('uid')]=[]
        for x in j.get('facts'):
            if str(x['fid']) in urls_tokens:
                facts[j.get('uid')] += urls_tokens[str(x['fid'])]
            if str(x['fid']) in html_titles:
                facts_html[j.get('uid')] += [html_titles[str(x['fid'])]]
            facts_fid[j.get('uid')] += [str(x['fid'])]
        if facts[j.get('uid')] == [] or facts_html[j.get('uid')] == [] or facts_fid[j.get('uid')] == []:
            facts.pop(j.get('uid'))
            facts_html.pop(j.get('uid'))
            facts_fid.pop(j.get('uid'))
del urls_tokens
del html_titles

##  Create facts file based on File: train.csv
#   users_for_predict contains userid not in the given File: train.csv
#   facts.txt: u1,u2,FidComCnt,URLComCnt
cont = 0
users_in_train = set()
with open('Training_facts.txt','w') as f_out:
    with open('data-train-dca/train.csv','r') as f_in:
        for line in tqdm(f_in):
            user1,user2 = line.strip().split(',')
            try:
                t = str(facts[user1]+facts[user2]).replace("'",'').replace("[",' ').replace("]",' ').replace(' ','')
            except:
                continue
            URLComCnt = len(set(facts[user1]) & set(facts[user2]))
            FidComCnt = len(set(facts_fid[user1]) & set(facts_fid[user2]))
            f_out.write('%s\t%s\t%s\t%s\t%s\n' % (user1,user2,t,str(FidComCnt),str(URLComCnt)))
            users_in_train.update([user1,user2])
            cont += 1
    cont_line = 0
    with open('negative_list.csv','r') as f_in:
        for line in tqdm(f_in):
            cont_line += 1
            if cont_line >= 100:
                cont_line = 0
                continue
            if cont_line > 10:
                continue
            user1,user2 = line.strip().split(',')
            try:
                t = str(facts[user1]+facts[user2]).replace("'",'').replace("[",' ').replace("]",' ').replace(' ','')
            except:
                continue
            URLComCnt = len(set(facts[user1]) & set(facts[user2]))
            FidComCnt = len(set(facts_fid[user1]) & set(facts_fid[user2]))
            f_out.write('%s\t%s\t%s\t%s\t%s\n' % (user1,user2,t,str(FidComCnt),str(URLComCnt)))
            users_in_train.update([user1,user2])
            cont += 1
print ("Total Pairs for training = {}".format(cont))

##  Create ###_train file
users_in_train_list = sorted(list(users_in_train))
print ("Number of user in train = {}".format(len(users_in_train_list)))
with open('facts_train.tsv','w') as f_out:
    for i in tqdm(range(len(users_in_train_list))):
        x = users_in_train_list[i]
        t = str(facts[x]).replace("'",'').replace("[",' ').replace("]",' ').replace(' ','')
        f_out.write("%s\t%s\n" % (x,t))
with open('fid_train.tsv','w') as f_out:
    for i in tqdm(range(len(users_in_train_list))):
        x = users_in_train_list[i]
        t = str(facts_fid[x]).replace("'",'').replace("[",' ').replace("]",' ').replace(' ','')
        f_out.write("%s\t%s\n" % (x,t))
with open('html_train.tsv','w') as f_out:
    for i in tqdm(range(len(users_in_train_list))):
        x = users_in_train_list[i]
        t = str(facts_html[x]).replace("'",'').replace("[",' ').replace("]",' ').replace(' ','')
        f_out.write("%s\t%s\n" % (x,t))
##  Create ###_test file
users_for_predict = set(facts.keys()).difference(users_in_train)
users_for_predict_list = sorted(list(users_for_predict))
print ("Number of user for test = {}".format(len(users_for_predict_list)))
with open('facts_test.tsv','w') as f_out:
    for i in tqdm(range(len(users_for_predict_list))):
        x = users_for_predict_list[i]
        t = str(facts[x]).replace("'",'').replace("[",' ').replace("]",' ').replace(' ','')
        f_out.write("%s\t%s\n" % (x,t))
with open('fid_test.tsv','w') as f_out:
    for i in tqdm(range(len(users_for_predict_list))):
        x = users_for_predict_list[i]
        t = str(facts_fid[x]).replace("'",'').replace("[",' ').replace("]",' ').replace(' ','')
        f_out.write("%s\t%s\n" % (x,t))
with open('html_test.tsv','w') as f_out:
    for i in tqdm(range(len(users_for_predict_list))):
        x = users_for_predict_list[i]
        t = str(facts_html[x]).replace("'",'').replace("[",' ').replace("]",' ').replace(' ','')
        f_out.write("%s\t%s\n" % (x,t))
##  Create user_### file for all users
#   339405 users
userlist = sorted(list(facts.keys()))
print ("Number of users with complete data = {}".format(len(userlist)))
with open('user_URL.txt','w') as f_out:
    for i in range(len(userlist)):
        x = userlist[i]
        t = str(facts[x]).replace("'",'').replace("[",' ').replace("]",' ').replace(' ','')
        f_out.write('%s\t%s\n' % (x,t))
with open('user_fid.txt','w') as f_out:
    for i in range(len(userlist)):
        x = userlist[i]
        t = str(facts_fid[x]).replace("'",'').replace("[",' ').replace("]",' ').replace(' ','')
        f_out.write('%s\t%s\n' % (x,t))
with open('user_html.txt','w') as f_out:
    for i in range(len(userlist)):
        x = userlist[i]
        t = str(facts_html[x]).replace("'",'').replace("[",' ').replace("]",' ').replace(' ','')
        f_out.write('%s\t%s\n' % (x,t))

del userlist
del users_in_train_list
del users_for_predict_list
del users_in_train
del users_for_predict
del facts
del facts_fid
del facts_html

print (datetime.today().strftime("%m/%d %H:%M:%S Prepare process finished"))

#
#
#

### TF-IDF matrix on user’s domains

##  Training set
#   urls
print ("Tfidf for urls Starts.")
users_train, row_text = {},[]
URL_tf_train = TfidfVectorizer(min_df=2, lowercase=False, sublinear_tf =True).fit(
map(lambda x: x.strip().split('\t')[-1],open('facts_train.tsv','r').readlines()))
print ("Size Vobab on URL_tf_train = {}".format(len(URL_tf_train.idf_)))
row_num = 0
with open('facts_train.tsv','r') as f_in:
    for line in tqdm(f_in):
        user, t = line.strip().split('\t')
        users_train[user] = row_num
        row_num += 1
        row_text.append(t)
URL_dt_train = URL_tf_train.transform(row_text)
print ("Document-term matrix on URL_train = {}".format(URL_dt_train.shape))
del row_text
#   html
print ("Tfidf for html Starts.")
row_text = []
Html_tf_train = TfidfVectorizer(min_df=2, lowercase=False, sublinear_tf =True).fit(
map(lambda x: x.strip().split('\t')[-1],open('html_train.tsv','r').readlines()))
print ("Size Vobab on Html_tf_train = {}".format(len(Html_tf_train.idf_)))
with open('html_train.tsv','r') as f_in:
    for line in tqdm(f_in):
        user, t = line.strip().split('\t')
        row_text.append(t)
Html_dt_train = Html_tf_train.transform(row_text)
print ("Document-term matrix on Html_train = {}".format(Html_dt_train.shape))
del row_text
#   fid
print ("Tfidf for fid Starts.")
row_text = []
Fid_tf_train = TfidfVectorizer(min_df=2, lowercase=False, sublinear_tf =True).fit(
map(lambda x: x.strip().split('\t')[-1],open('fid_train.tsv','r').readlines()))
print ("Size Vobab on Fid_tf_train = {}".format(len(Fid_tf_train.idf_)))
with open('fid_train.tsv','r') as f_in:
    for line in tqdm(f_in):
        user, t = line.strip().split('\t')
        row_text.append(t)
Fid_dt_train = Fid_tf_train.transform(row_text)
print ("Document-term matrix on Fid_train = {}".format(Fid_dt_train.shape))
del row_text

##  Testing set

# tf_test = TfidfVectorizer(min_df=2, lowercase=False, sublinear_tf =True).fit(
# map(lambda x: x.strip().split('\t')[-1],open('facts_test.tsv','r').readlines()))
# print ("Size Vobab on tf_test = {}".format(len(tf_test.idf_)))

#
# users_test, row_text = [], []
# with open('facts_test.tsv') as f_in:
#     for line in tqdm(f_in):
#         user, t = line.strip().split('\t')
#         users_test.append(user)
#         row_text.append(t)
# dtmatrix_test = tf_test.transform(row_text)
# print ("Document-term matrix on test = {}".format(dtmatrix_test.shape))
# del row_text


### Feature Engineering

with open('Metric/Train_features.txt','w') as f_out:
    with open('Training_facts.txt','r') as f_in:
        for line in tqdm(f_in):
            user1, user2, t,FidComCnt, URLComCnt = line.strip().split('\t')
            if users_train[user1] == users_train[user2]:
                sys.exit("Error in Tfidf users_train")
            # URLsim
            user1_Tfidf = URL_dt_train[users_train[user1]].toarray()
            user2_Tfidf = URL_dt_train[users_train[user2]].toarray()
            numerator = np.dot(user1_Tfidf,user2_Tfidf.transpose()).item(0)
            denominator = (np.sqrt(np.dot(user1_Tfidf,user1_Tfidf.transpose()).item(0))*
                        np.sqrt(np.dot(user2_Tfidf,user2_Tfidf.transpose()).item(0)))
            URLSim = str(numerator/denominator)
            # Fidsim
            user1_Tfidf = Fid_dt_train[users_train[user1]].toarray()
            user2_Tfidf = Fid_dt_train[users_train[user2]].toarray()
            numerator = np.dot(user1_Tfidf,user2_Tfidf.transpose()).item(0)
            denominator = (np.sqrt(np.dot(user1_Tfidf,user1_Tfidf.transpose()).item(0))*
                        np.sqrt(np.dot(user2_Tfidf,user2_Tfidf.transpose()).item(0)))
            FidSim = str(numerator/denominator)
            # Docsim
            user1_Tfidf = Html_dt_train[users_train[user1]].toarray()
            user2_Tfidf = Html_dt_train[users_train[user2]].toarray()
            numerator = np.dot(user1_Tfidf,user2_Tfidf.transpose()).item(0)
            denominator = (np.sqrt(np.dot(user1_Tfidf,user1_Tfidf.transpose()).item(0))*
                        np.sqrt(np.dot(user2_Tfidf,user2_Tfidf.transpose()).item(0)))
            HtmlSim = str(numerator/denominator)

            f_out.write("%s\t%s\t%s\t%s\t%s\t%s\t%s\n" % (user1,user2,HtmlSim,FidSim,URLSim,FidComCnt,URLComCnt))

del URL_dt_train
del Fid_dt_train
del Html_dt_train
print (datetime.today().strftime("%m/%d %H:%M:%S Data Engineering finished"))
