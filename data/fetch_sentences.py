import json
import requests
from pymongo import MongoClient
from google.cloud import translate
import codecs
from googletrans import Translator
import time
import html
import pandas as pd
import inflect
import re

inflect = inflect.engine()

app_id = '991ba59d'
app_key = '73858cc4ebebad8f8bf65b84aa207ccf'

result = {"data": []}
client = translate.Client()

counter = 0
char = 0


def findWholeWord(w):
    return re.compile(r'\b({0})\b'.format(w), flags=re.IGNORECASE).search


words_done = []

wordsSkip = ['bacon', 'beef', 'chicken', 'ham', 'hamburger', 'hot dog', 'pork', 'sausage', 'steak', 'turkey', 'veal',
             'apple', 'apricot', 'banana', 'blackberry', 'blueberry', 'cherry', 'currant', 'fig', 'grape', 'grapefruit',
             'kiwi', 'lemon', 'lime', 'melon', 'nectarine', 'peach', 'pear', 'pineapple', 'plum', 'pomegranate',
             'prune', 'raspberry', 'strawberry', 'tangerine', 'watermelon', 'apple pie', 'cake', 'candy', 'fruit',
             'ice cream', 'muffin', 'pie', 'pudding', 'alligator', 'ant', 'bee', 'bird', 'camel', 'cat', 'cheetah',
             'chimpanzee', 'cow', 'crocodile', 'deer', 'dog', 'dolphin', 'duck', 'eagle', 'elephant', 'fish', 'fly',
             'fox', 'frog', 'giraffe', 'goat', 'goldfish', 'hamster', 'hippopotamus', 'horse', 'kangaroo', 'kitten',
             'leopard', 'lion', 'lizard', 'monkey', 'octopus', 'ostrich', 'otter', 'owl', 'oyster', 'panda', 'parrot',
             'pelican', 'pig', 'pigeon', 'porcupine', 'puppy', 'rabbit', 'rat', 'reindeer', 'rhinoceros', 'rooster',
             'scorpion', 'shark', 'sheep', 'shrimp', 'snail', 'snake', 'sparrow', 'spider', 'squid', 'squirrel',
             'tiger', 'toad', 'tortoise', 'turtle', 'vulture', 'walrus', 'weasel']

food = pd.read_csv("food.csv", index_col=None, header=0)
animals = pd.read_csv("animals.csv", index_col=None, header=0)
colors = pd.read_csv("colors.csv", index_col=None, header=0)
clothes = pd.read_csv("clothes.csv", index_col=None, header=0)

frames = [food, animals, colors, clothes]

words_collection = pd.concat(frames)

for index, document in words_collection.iterrows():

    if document["en"] not in wordsSkip:
        skip = False

        element = {"id": "", "lexicalCategory": "",
                   "en": {"word": "", "sentences": [], "difficulty_level": 0},
                   "fr": {"word": "", "sentences": [], "difficulty_level": 0},
                   'es': {"word": "", "sentences": [], "difficulty_level": 0},
                   'de': {"word": "", "sentences": [], "difficulty_level": 0},
                   "url": "", "topic": ""}

        word = document["en"]
        language = 'en'
        word_id = word

        element["id"] = word
        element["url"] = document["url"]
        element["topic"] = document["topic"]

        url = 'https://od-api.oxforddictionaries.com:443/api/v1/entries/' + language + '/' + word_id.lower()
        r = requests.get(url, headers={'app_id': app_id, 'app_key': app_key})
        counter += 1

        try:
            data = json.dumps(r.json())
            data = json.loads(data)
            data = data["results"][0]
        except Exception as e:
            print("skip " + word)
            skip = True

        if not skip:
            print(data["id"])

            element["lexicalCategory"] = data["lexicalEntries"][0]["lexicalCategory"]

            url = 'https://od-api.oxforddictionaries.com:443/api/v1/entries/' + language + '/' + word_id.lower() + '/sentences'
            r = requests.get(url, headers={'app_id': app_id, 'app_key': app_key})
            counter += 1

            data = json.dumps(r.json())
            data = json.loads(data)
            data = data["results"][0]

            sentences = [elem["text"] for elem in data["lexicalEntries"][0]["sentences"] if
                         findWholeWord(word)(elem["text"].lower()) is not None or
                         findWholeWord(inflect.plural(word))(elem["text"].lower()) is not None]

            for s in sentences:
                char += len(s)

            if len(sentences) != 0:
                size = min(len(sentences), 4)
                sentences = sentences[:size]

            element["en"]["sentences"].append(sentences)

            french_sentences = client.translate(sentences, target_language='fr', source_language='en')
            spanish_sentences = client.translate(sentences, target_language='es', source_language='en')
            german_sentences = client.translate(sentences, target_language='de', source_language='en')

            for s in german_sentences:
                element["de"]["sentences"].append(html.unescape(s["translatedText"]))

            for s in french_sentences:
                element["fr"]["sentences"].append(html.unescape(s["translatedText"]))

            for s in spanish_sentences:
                element["es"]["sentences"].append(html.unescape(s["translatedText"]))

            element["en"]["word"] = word
            element["fr"]["word"] = document["fr"]
            element["es"]["word"] = document["es"]
            element["de"]["word"] = document["de"]

            result["data"].append(element)

            with open('data3.json', 'w', encoding='utf8') as fp:
                json.dump(result, fp, ensure_ascii=False)

            fp.close()

            words_done.append(word)

            if char > 800000:
                print("sleeping for 100 sec")
                time.sleep(100)
                char = 0

            elif (counter % 50) == 0:
                print("sleeping for 75 sec")
                time.sleep(75)

            print(char, counter)
            print(words_done)
            print(len(words_done))
