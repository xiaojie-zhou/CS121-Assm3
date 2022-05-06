import json
import math
from timeit import default_timer

from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize

with open('Hashmap.txt', 'r', encoding='utf-8') as h:
    hashmap = json.load(h)
with open("report.txt", "r", encoding='utf-8') as rep:
    index = rep.readlines()[-1]
    total = int(index.rstrip('\n').split()[-1])
    index = total // 20000 + 1


def tokenizer(text):
    terms_result = []
    ps = PorterStemmer()
    words = word_tokenize(text)
    for word in words:
        if word.isalnum():
            term = ps.stem(word)
            terms_result.append(term)
    return terms_result


def tfidf(tf, df, N):
    idf = math.log(N / df, 10)
    return (1 + math.log(tf, 10)) * idf


def read_term(ct,termdict):
    st = tokenizer(ct)  # selected term list
    tfhelpdict = {}
#     for x in range(1, index + 1):
#         name = "index" + str(x) + ".txt"
#         with open(name, "r", encoding="utf-8") as ind:
#             js = json.load(ind)
    for js in termdict:
        for term in st:
            if term in termdict[js]:  # term:docid:tf
                if term in tfhelpdict.keys():
                    tfhelpdict[term].update(termdict[js][term])
                else:                    
                    tfhelpdict[term] = termdict[js][term]
                                
    for term, doc in tfhelpdict.items():
        ternum = len(doc)
        idf = ternum / total
        for docid, v in doc.items():
            score = tfidf(v, idf, total)
            tfhelpdict[term][docid] = score
    
    tfdict = {}
    for term in tfhelpdict:
        for docid in tfhelpdict[term]:
            if docid not in tfdict:
                tfdict[docid] = tfhelpdict[term][docid]
            else:
                tfdict[docid] += tfhelpdict[term][docid]
    
    nrtl = []
    for x, y in tfdict.items():  # {docid:tfidf}
        nrtl.append((x, y))
    nrtl.sort(key=lambda t: -t[1])
    rtnl = []

    for x in nrtl:
        rtnl.append(x[0])
    
    for i in range(len(rtnl)):
        rtnl[i] = hashmap[rtnl[i]]
    return rtnl[0:20]


if __name__ == "__main__":
    print("Initiating")
    termdict = {}
    for x in range(1, index + 1):
        name = "index" + str(x) + ".txt"
        with open(name, "r", encoding="utf-8") as ind:
            js = json.load(ind)
        termdict[x]=js
    while True:
        term = input("Please enter your query: ")
        if len(term) > 0:
            if term == 'Quit':
                break
            try:
                start = default_timer()
                temp = read_term(term,termdict)
                end = default_timer()
                if len(temp) > 0:
                    print("Query results: ")
                    for i, url in enumerate(temp):
                        print(i + 1, url)
                print(str((end - start) * 1000) + " ms")
            except KeyError:
                print("Query not found.")
