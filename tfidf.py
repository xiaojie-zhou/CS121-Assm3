import json
import math


def tfidf(tf, df, N):
    idf = math.log(N / df, 10)
    return (1 + math.log(tf, 10)) * idf


if __name__ == "__main__":
    with open("report.txt", "r", encoding="utf-8") as rep:
        index = rep.readlines()[-1]
        total = int(index.rstrip('\n').split()[-1])
        index = total // 3000 + 1

    for x in range(1, index + 1):
        name = "index" + str(x) + ".txt"
        with open(name, "r", encoding="utf-8") as ind:
            js = json.load(ind)
        inverted_index = js

        for sterm, sdoc in inverted_index.items():
            NumODoc = len(sdoc)
            for doid in sdoc:
                otf = tfidf(sdoc[doid], NumODoc, total)
                sdoc[doid] = otf
        with open(name, "w", encoding="utf-8") as ind:
            ind.write(json.dumps(inverted_index))
