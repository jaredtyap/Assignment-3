from bs4 import BeautifulSoup
import nltk
from nltk.stem import PorterStemmer
from nltk.corpus import words
import json 
import os

ps = PorterStemmer()
path = 'testing/'
index = {}
index['the'] = 0
total_doc = 0
for filename in os.listdir(path):
    with open(os.path.join(path,filename),'r') as f:
        #file = open(f,)
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
            flag=0

            for i in list(index):
                if x == i:
                    index[x] +=1
                    flag=1
            
            if flag == 0:
                index[x] = 1
            else: 
                flag = 0
                

print(dict(sorted(index.items(), key=lambda item: item[1])))
print(total_doc)