from bs4 import BeautifulSoup
import nltk
from nltk.stem import PorterStemmer
from nltk.corpus import words
import json 
import os
import numpy as np


count = {}
ps = PorterStemmer()
def text_processing():
    path = 'source/'
    total_doc = 0
    for filename in os.listdir(path):
        with open(os.path.join(path,filename),'r') as f:
            total_doc +=1
            data = json.load(f)
            soupdata = data['content']
            soup = BeautifulSoup(soupdata, 'html.parser')
            # bold_text=soup.find_all(["b","strong","h1","h2","h3","title"])
            # bold_text_list =[]
            # for i in bold_text:
            #     bold_text_list.append(i.text)
            
            raw_data = soup.get_text()
            tokenizer = nltk.RegexpTokenizer(r'\w{2,}')
            # bold_text_2 =' '.join(map(str, bold_text_list))
            # bold_text_token = tokenizer.tokenize(bold_text_2)
            tokens = tokenizer.tokenize(raw_data)
            # tokens = tokens + bold_text_token
            word_count(tokens,total_doc,count)
            print(total_doc)
    return count, total_doc
def word_count(tokens,total_doc,count):
    for x in tokens:
        x = x.lower()
        x = ps.stem(x)
        try:
            count[x].add(total_doc)
        except: 
            count[x] = {total_doc}
    return count
def tf_idf(sub_index,freq_count,total_doc):
    
    tf_idf = {}
    for x in sub_index:
        tf = 1+np.log(sub_index[x])
        try:
            idf = np.log(total_doc/freq_count[x])
        except:
            idf = 2
        tf_idf[x] = tf*idf
    return tf_idf

def counting(final_count):
    for i in final_count: 
        try:
            final_count[i] = len(final_count[i])
        except:
            final_count[i] = 1
    return final_count
def final_adding(final_count,total_doc):
    path = 'source/'
    index = {}
    index['the'] = 0
    counter = 0
    count = {}
    for filename in os.listdir(path):
        with open(os.path.join(path,filename),'r') as f:
            counter +=1
            data = json.load(f)
            soupdata = data['content']
            url = data['url']
            soup = BeautifulSoup(soupdata, 'html.parser')
            bold_text=soup.find_all(["b","strong","h1","h2","h3","title"])
            bold_text_list =[]
            for i in bold_text:
                bold_text_list.append(i.text)
            raw_data = soup.get_text()
            tokenizer = nltk.RegexpTokenizer(r'\w{2,}')
            bold_text_2 =' '.join(map(str, bold_text_list))
            bold_text_token = tokenizer.tokenize(bold_text_2)
            tokens = tokenizer.tokenize(raw_data)
            tokens = tokens + bold_text_token
            freq_count = counting(final_count)
            sub_index = {}
            for x in tokens:
                x = x.lower()
                x = ps.stem(x)
                flag=0
                try:
                    sub_index[x] +=1
                except:
                    sub_index[x] = 1
            sub_index=tf_idf(sub_index,freq_count,total_doc)
            for y in sub_index:
                try:
                    index[y].append((url,sub_index[y]))
                except:
                    index[y] = [(url,sub_index[y])]
            print(counter)
    return index
count,total_doc = text_processing()
index = final_adding(count,total_doc)
f = open("index.txt","w", encoding="utf8")
f.write(str(index))
f.close()