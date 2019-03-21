import json
import requests
from pymongo import MongoClient
from google.cloud import translate
import codecs
from googletrans import Translator
import time
import html

client = MongoClient(port=27017)

db = client.loloDB
voc_collection = db["vocabulary"]

voc_collection.remove({})

for file in ["data2.json", "data3.json", "data4.json", "data5.json"]:
    with open(file) as f:
        data = json.load(f)

        data = data["data"]
        for word in data:
            voc_collection.insert(word)

