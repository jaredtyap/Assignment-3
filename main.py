from bs4 import BeautifulSoup
import nltk
from nltk.stem import PorterStemmer
import json 
import os

ps = PorterStemmer()
path = 'testing/'
index = {}
for filename in os.listdir(path):
    with open(os.path.join(path,filename),'r') as f:
        #file = open(f,)
        data = json.load(f)
        soupdata = data['content']
        print(data['url'])
        soup = BeautifulSoup(soupdata, 'html.parser')
        raw_data = soup.get_text()
        tokenizer = nltk.RegexpTokenizer(r'\w+')
        tokens = tokenizer.tokenize(raw_data)
        for x in tokens:
            if len(index) == 0:
                index[x] = 1
            else:
                for i in list(index):
                    if x == i:
                        index[i] +=1
                    else:
                        index[x] = 1

print(index)