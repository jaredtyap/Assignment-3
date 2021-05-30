import nltk
import os
import string
import numpy as np
import copy
import pandas as pd
import pickle
import re
import math
from bs4 import BeautifulSoup
from nltk.corpus import words
from nltk.tokenize import word_tokenize
from nltk.stem import SnowballStemmer
from collections import Counter
import json 
import os





count = {}
query_index = {}

ps = SnowballStemmer("english")
def text_processing():
    path = 'testingfiles/'
    query_counter = 0
    total_doc = 0
    for filename in os.listdir(path):
        with open(os.path.join(path,filename),'r') as f:
            total_doc +=1
            data = json.load(f)
            soupdata = data['content']
            encode = data['encoding']
            soup = BeautifulSoup(soupdata, 'html.parser', from_encoding=encode)	
            raw_data = soup.get_text()
            tokenizer = nltk.RegexpTokenizer(r'\w{2,}')
            tokens = tokenizer.tokenize(raw_data)
            word_count(tokens,total_doc,count, query_counter)
            print(total_doc)
    return count, total_doc

def word_count(tokens,total_doc,count, query_counter):
    for x in tokens:
        x = x.lower()
        x = ps.stem(x)
        try:
            count[x].add(total_doc)
        except: 
            count[x] = {total_doc}
        if x in query_index:
            continue
        else:
            query_index[x] = query_counter
            query_counter += 1
        
def doc_freq(word):
    c = 0
    try:
        c = DFcount[word]
    except:
        pass
    return c

def tf_idf(tokens):
    tf_idf = {}
    for i in range(N):
        counter = Counter(tokens)
        words_count = len(tokens)
        
        for token in np.unique(tokens):
            
            tf = counter[token]/words_count
            df = doc_freq(token)
            idf = np.log((N+1)/(df+1))
            
            tf_idf[token]= tf*idf

        return tf_idf

def final_adding():
    path = 'testingfiles/'
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
            
            sub_index = {}
            for x in tokens:
                x = x.lower()
                x = ps.stem(x)
                try:
                    sub_index[x] +=1
                except:
                    sub_index[x] = 1
            sub_index=tf_idf(tokens)
            for y in sub_index:
                try:
                    index[y].append((url,sub_index[y]))
                except:
                    index[y] = [(url,sub_index[y])]
            print(counter)
    return index

def counting(final_count):
    for i in final_count: 
        try:
            final_count[i] = len(final_count[i])
        except:
            final_count[i] = 1
    return final_count

DF, N = text_processing() #N = total number of docs.  DF is the dictionary of words:number of docs the words appear in
DFcount = counting(DF)
total_vocab_size = len(DF)
total_vocab = [x for x in DF]
index = final_adding()
f = open("indexer.txt","w", encoding="utf8")
f.write(str(index))
f.close()
f = open("stats.txt", "w", encoding="utf8" )
f.write(str(N))
f.write("\n")
f.write(str(total_vocab_size))
f.close()
f = open("df.txt", "w", encoding="utf8")
f.write(str(DFcount))
f.close()
f = open("vocab.txt", "w", encoding="utf8")
f.write(str(total_vocab))
f.close()
f = open("query_index.txt", 'w', encoding ="utf8")
f.write(str(query_index))
f.close()

def vectorize():
    # f = open("vocab.txt", "r", encoding = "utf8")
    # total_vocab = f.read()
    # with open("index.txt", "r", encoding="utf8") as y:
    #     index = y.read()    
    D = np.zeros((N, total_vocab_size))
    for i in index:
        try:
            ind = total_vocab.index(i[1])
            D[i[0]][ind] = index[i]
        except:
            pass
    return D