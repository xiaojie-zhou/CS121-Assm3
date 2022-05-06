import json
import math
import os
import re
from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize
from urllib.parse import urlparse
from bs4 import BeautifulSoup
import validators


def tokenizer(text):
    skip = ["url", "http", "https", "content"]
    terms_result = []
    ps = PorterStemmer()
    words = word_tokenize(text)
    for word in words:
        if word not in skip and word.isalnum():
            term = ps.stem(word)
            terms_result.append(term)

    return terms_result


def is_valid(url):
    try:
        parsed = urlparse(url)
        if parsed.scheme not in {"http", "https"}:
            return False
        if not validators.url(url):
            return False
        return not re.match(
            r".*\.(css|js|bmp|gif|jpe?g|ico"
            + r"|png|tiff?|mid|mp2|mp3|mp4"
            + r"|wav|avi|mov|mpeg|ram|m4v|mkv|ogg|ogv|pdf|sql"
            + r"|ps|eps|tex|ppt|pptx|doc|docx|xls|xlsx|names"
            + r"|data|dat|exe|bz2|tar|msi|bin|7z|psd|dmg|iso"
            + r"|epub|dll|cnf|tgz|sha1"
            + r"|thmx|mso|arff|rtf|jar|csv"
            + r"|rm|smil|wmv|swf|wma|zip|rar|gz|npy)$", parsed.path.lower())
    except:
        return False


def tfidf(tf, df, N):
    idf = math.log(N / df, 10)
    return (1 + math.log(tf, 10)) * idf


if __name__ == "__main__":
    # {term : {docID: freq}}
    inverted_index = {}
    hashmap = {}
    pagecount = 0

    path = os.getcwd() + "/DEV"

    for folderloc in os.listdir(path):
        if str(folderloc) == ".DS_Store":
            continue

        p_path = path + '/' + str(folderloc)

        for file in os.listdir(p_path):
            f_path = p_path + '/' + file

            f = open(f_path)
            # f = open("/Users/XiaojieZhou/CS121/Assignment3/CS121-Assm3/DEV/cbcl_ics_uci_edu/736d048cbf05c6c1a390e0c1a47b04891c01398ea057bcdb509654bc4289dbd3.json")
            js = json.load(f)
            print(pagecount, f_path, js["url"])

            if not is_valid(js["url"]):
                continue

            html_str = js["content"]

            html = BeautifulSoup(html_str, 'html.parser')
            words_str = html.getText()

            terms = tokenizer(words_str)


            if js["url"] not in hashmap.values():
                hashmap[hash(js["url"])] = js["url"]

            for i in terms:
                if i not in inverted_index.keys():
                    inverted_index[i] = {hash(js["url"]): 1 }
                elif hash(js["url"]) not in inverted_index[i].keys():
                    inverted_index[i][hash(js["url"])] = 1
                else:
                    inverted_index[i][hash(js["url"])] += 1

            f.close()
            pagecount += 1

            if pagecount % 20000 == 0:
                filep = open(f"index{pagecount // 20000}.txt", "w")
                filep.write(json.dumps(inverted_index))
                filep.close()
                inverted_index = {}

    filep = open(f"index{(pagecount // 20000) + 1}.txt", "w")
    filep.write(json.dumps(inverted_index))
    filep.close()
    inverted_index = {}

    with open("Hashmap.txt", 'w', encoding="utf-8") as out:
        out.write(json.dumps(hashmap))
