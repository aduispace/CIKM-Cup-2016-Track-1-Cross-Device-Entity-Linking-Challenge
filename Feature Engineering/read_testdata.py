import json
import numpy as np
import sys
from tqdm import tqdm   # install tqdm package(a progress meter) by
                        # enter 'pip install tqdm' in terminal
from datetime import datetime
from sklearn.feature_extraction.text import TfidfVectorizer


#  File: urls.csv
  urls_tokens: [fid[urls],...] Only take 1 levle urls
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

cont = 0
users_in_test = set()
with open('Testing_facts.txt','w') as f_out:
    with open('Knnlist.csv','r') as f_in:
        for line in tqdm(f_in):
            user1,user2 = line.strip().split(',')
            try:
                t = str(facts[user1]+facts[user2]).replace("'",'').replace("[",' ').replace("]",' ').replace(' ','')
            except:
                continue
            URLComCnt = len(set(facts[user1]) & set(facts[user2]))
            FidComCnt = len(set(facts_fid[user1]) & set(facts_fid[user2]))
            f_out.write('%s\t%s\t%s\t%s\t%s\n' % (user1,user2,t,str(FidComCnt),str(URLComCnt)))
            users_in_test.update([user1,user2])
            cont += 1
print ("Total Pairs for testing = {}".format(cont))

del urls_tokens
del html_titles
del facts
del facts_fid
del facts_html
################################################################################

#   urls
print ("Tfidf for urls Starts.")
users_test, row_text = {},[]
URL_test = TfidfVectorizer(min_df=2, lowercase=False, sublinear_tf =True).fit(
map(lambda x: x.strip().split('\t')[-1],open('facts_test.tsv','r').readlines()))
print ("Size Vobab on URL_test = {}".format(len(URL_test.idf_)))
row_num = 0
with open('facts_test.tsv','r') as f_in:
    for line in tqdm(f_in):
        user, t = line.strip().split('\t')
        users_test[user] = row_num
        row_num += 1
        row_text.append(t)
URL_dt_test = URL_test.transform(row_text)
print ("Document-term matrix on URL_test = {}".format(URL_dt_test.shape))
#   htmls
print ("Tfidf for html Starts.")
row_text = []
html_test = TfidfVectorizer(min_df=2, lowercase=False, sublinear_tf =True).fit(
map(lambda x: x.strip().split('\t')[-1],open('html_test.tsv','r').readlines()))
print ("Size Vobab on html_test = {}".format(len(html_test.idf_)))
with open('html_test.tsv','r') as f_in:
    for line in tqdm(f_in):
        user, t = line.strip().split('\t')
        row_text.append(t)
html_dt_test = html_test.transform(row_text)
print ("Document-term matrix on html_test = {}".format(html_dt_test.shape))
#   fid
print ("Tfidf for fid Starts.")
row_text = []
fid_test = TfidfVectorizer(min_df=2, lowercase=False, sublinear_tf =True).fit(
map(lambda x: x.strip().split('\t')[-1],open('fid_test.tsv','r').readlines()))
print ("Size Vobab on fid_test = {}".format(len(fid_test.idf_)))
with open('fid_test.tsv','r') as f_in:
    for line in tqdm(f_in):
        user, t = line.strip().split('\t')
        row_text.append(t)
fid_dt_test = fid_test.transform(row_text)
print ("Document-term matrix on fid_test = {}".format(fid_dt_test.shape))
del row_text


with open('Test_features.txt','w') as f_out:
    with open('Testing_facts.txt','r') as f_in:
        for line in tqdm(f_in):
            user1, user2, t,FidComCnt, URLComCnt = line.strip().split('\t')
            if users_test[user1] == users_test[user2]:
                # sys.exit("Error in Tfidf users_test")
                continue
            # URLsim
            user1_Tfidf = URL_dt_test[users_test[user1]].toarray()
            user2_Tfidf = URL_dt_test[users_test[user2]].toarray()
            numerator = np.dot(user1_Tfidf,user2_Tfidf.transpose()).item(0)
            denominator = (np.sqrt(np.dot(user1_Tfidf,user1_Tfidf.transpose()).item(0))*
                        np.sqrt(np.dot(user2_Tfidf,user2_Tfidf.transpose()).item(0)))
            URLSim = str(numerator/denominator)
            # Fidsim
            user1_Tfidf = fid_dt_test[users_test[user1]].toarray()
            user2_Tfidf = fid_dt_test[users_test[user2]].toarray()
            numerator = np.dot(user1_Tfidf,user2_Tfidf.transpose()).item(0)
            denominator = (np.sqrt(np.dot(user1_Tfidf,user1_Tfidf.transpose()).item(0))*
                        np.sqrt(np.dot(user2_Tfidf,user2_Tfidf.transpose()).item(0)))
            FidSim = str(numerator/denominator)
            # Docsim
            user1_Tfidf = html_dt_test[users_test[user1]].toarray()
            user2_Tfidf = html_dt_test[users_test[user2]].toarray()
            numerator = np.dot(user1_Tfidf,user2_Tfidf.transpose()).item(0)
            denominator = (np.sqrt(np.dot(user1_Tfidf,user1_Tfidf.transpose()).item(0))*
                        np.sqrt(np.dot(user2_Tfidf,user2_Tfidf.transpose()).item(0)))
            HtmlSim = str(numerator/denominator)

            f_out.write("%s\t%s\t%s\t%s\t%s\t%s\t%s\n" % (user1,user2,HtmlSim,FidSim,URLSim,FidComCnt,URLComCnt))
