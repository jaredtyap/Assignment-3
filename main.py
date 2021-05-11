from bs4 import BeautifulSoup
import nltk
from nltk.stem import PorterStemmer
from nltk.corpus import words
import json 
import os

ps = PorterStemmer()
path = 'TestFiles/'
index = {}
index['the'] = 0
total_doc = 0
for filename in os.listdir(path):
    with open(os.path.join(path,filename),'r') as f:
        #file = open(f,)
        total_doc +=1
        data = json.load(f)
        soupdata = data['content']
        soup = BeautifulSoup(soupdata, 'html.parser')
        raw_data = soup.get_text()
        tokenizer = nltk.RegexpTokenizer(r'\w{2,}')
        tokens = tokenizer.tokenize(raw_data)
        print(f)
        for x in tokens:
            x = x.lower()
            flag=0
            if x in index.keys():
                    index[x] +=1
                    flag=1
                    continue
            if flag == 0:
                index[x] = 1
            else: 
                flag = 0
        print(total_doc)
f = open("index.txt","w", encoding="utf8")
f.write(str(index))
f.close()
print(len(index))
print(total_doc)