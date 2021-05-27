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
        soup = BeautifulSoup(soupdata, 'html.parser')
        raw_data = soup.get_text()
        tokenizer = nltk.RegexpTokenizer(r'\w{2,}')
        tokens = tokenizer.tokenize(raw_data)
        for x in tokens:
            x = x.lower()
            x = ps.stem(x)
            flag=0
            if x in index.keys():
                if isinstance(index[x],int):
                    counter = index[x]
                else: 
                    counter = len(index[x])
                for i in range(0,counter,1):
                    print(index[x][i][0])
                    if total_doc == index[x][i][0]:
                        curr = index[x][i][1]
                        curr +=1
                        index[x][i] = (total_doc,curr)
                    else:
                        index[x].append((total_doc,1))
                    flag=1
                    continue
            if flag == 0:
                index[x] = [(total_doc,1)]
            else: 
                flag = 0
        print(total_doc)
f = open("index.txt","w", encoding="utf8")
f.write(str(index))
f.close()
print(len(index))
print(total_doc)