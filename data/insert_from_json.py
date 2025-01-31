import json
from pymongo import MongoClient


client = MongoClient(port=27017)

db = client.loloDB
voc_collection = db["vocabulary"]

def check_duplicate():
    l = []
    for word in voc_collection.find():
        if word in l:
            print(word)
        l.append(word)

voc_collection.remove({})

for file in ["data_ok.json"]:
    with open(file) as f:
        data = json.load(f)

        for word in data:
            voc_collection.insert(word)

