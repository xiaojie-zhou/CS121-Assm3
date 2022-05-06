import json

with open("report.txt", 'w', encoding="utf-8") as report:
    f = open("Hashmap.txt", "r")
    hashmap = json.load(f)
    terms = []
    for x in range(1, 4):
        name = "index" + str(x) + ".txt"
        with open(name, "r", encoding="utf-8") as ind:
            js = json.load(ind)
            terms.extend(js.keys())
    terms = set(terms)
    report.write("Unique terms: " + str(len(terms)))
    report.write('\nTotal Pages: ' + str(len(hashmap.keys())))
