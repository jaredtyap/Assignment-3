import numpy as np
from collections import Counter
import json 
import ast 

def read_data():
    f = open("stats.txt","r", encoding="utf8")
    N = f.readline()
    total_vocab_size = f.readline()
    f.close()
    N = N.strip('\n')
    N = int(N)
    total_vocab_size = int(total_vocab_size)
    with open("df.txt", "r", encoding="utf8") as x:
        temp = x.read()
    DF = ast.literal_eval(temp)
    return N, total_vocab_size, DF


def cosine_sim(a, b):
    cos_sim = np.dot(a, b)/(np.linalg.norm(a)*np.linalg.norm(b))
    return cos_sim


# def gen_vector(tokens, total_vocab_size):

#     Q = np.zeros(total_vocab_size)
    
#     counter = Counter(tokens)
#     words_count = len(tokens)

#     query_weights = {}
    
#     for token in np.unique(tokens):
        
#         tf = counter[token]/words_count
#         df = doc_freq(token)
#         idf = math.log((N+1)/(df+1))

#         try:
#             ind = total_vocab.index(token)
#             Q[ind] = tf*idf
#         except:
#             pass
#     return Q

def vectorize():
    f = open("vocab.txt", "r", encoding = "utf8")
    total_vocab = f.read()
    with open("index.txt", "r", encoding="utf8") as y:
        index = y.read()    
        D = np.zeros((N, total_vocab_size))
        for i in index:
            try:
                ind = total_vocab.index(i)
                D[i[0]][ind] = index[i]
            except:
                pass
    return D


N, total_vocab_size, DF = read_data()
print(vectorize())