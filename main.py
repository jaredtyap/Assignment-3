from bs4 import BeautifulSoup
import nltk
from nltk.stem import PorterStemmer
from nltk.corpus import words
import json 
import os

ps = PorterStemmer()
path = 'source/'
index = {}
index['the'] = 0
total_doc = 0
for filename in os.listdir(path):
    with open(os.path.join(path,filename),'r') as f:
        #file = open(f,)
        print(f)
        total_doc +=1
        data = json.load(f)
        soupdata = data['content']
        print(data['url'])
        soup = BeautifulSoup(soupdata, 'html.parser')
        raw_data = soup.get_text()
        tokenizer = nltk.RegexpTokenizer(r'\w{2,}')
        tokens = tokenizer.tokenize(raw_data)
        for x in tokens: 
            x = x.lower()
            x = ps.stem(x)
            flag=0
            for i in list(index):
                if x == i:
                    index[x] +=1
                    flag=1
                    break
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