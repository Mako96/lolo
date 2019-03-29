from pymongo import MongoClient
from bson.objectid import ObjectId
from collections import Counter
from itertools import chain
import json
import random


class JSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        return json.JSONEncoder.default(self, o)


class DBController:

    def __init__(self):
        client = MongoClient(port=27017)
        self.db = client.loloDB
        self.user_collection = self.db["users"]
        self.voc_collection = self.db["vocabulary"]
        self.lang_collection = self.db["languages"]

    def insertUser(self, user_email, language_to_learn):
        """ Inserts an email address in the user collection
            Returns the userID if it succeeds else None"""
        if not self.doesUserExist(user_email):
            query = {"email": user_email, "learning_language": language_to_learn, "interests": [], "taughtWords": [],
                     "testedWords": []}
            self.user_collection.insert_one(query)
            userID = self.user_collection.find_one({"email": user_email}, {'_id': 1})
            return str(userID["_id"])
        else:
            return None

    def doesUserExist(self, user_email):
        """Returns the userID if the user exists else None"""
        query = {"email": user_email}
        userID = self.user_collection.find_one({"email": user_email}, {'_id': 1})
        if userID:
            return str(userID["_id"])
        else:
            return None

    def doesUserExistByID(self, user_ID):
        """Returns the userID if the user exists else None"""
        if not ObjectId.is_valid(user_ID):
            return False

        userID = self.user_collection.find_one({"_id": ObjectId(user_ID)}, {'_id': 1})
        if userID:
            return True
        else:
            return False

    def getInterests(self, user_ID):
        """Returns a list of the user interests.
           Returns None if the user doesn't exist"""
        if not self.doesUserExistByID(user_ID):
            return None
        res = self.user_collection.find_one(
            {"_id": ObjectId(user_ID)},
            {"interests": 1, '_id': 0}
        )
        return res["interests"]

    def setInterests(self, user_ID, interests):
        """Sets the interests of a user. Takes a list of interests and the email as arguments.
           Returns True if it succeeds, else false"""
        if self.doesUserExistByID(user_ID):
            self.user_collection.update(
                {"_id": ObjectId(user_ID)},
                {"$set": {"interests": interests}}
            )
            return True
        return False

    def insertLanguages(self, languages):
        """Insert new languages in the language collection"""
        for lang in languages:
            self.lang_collection.insert_one(lang)

    def getLearningLanguages(self):
        """Returns all the possible languages to learn"""
        languages = self.lang_collection.find({},
                                              {"_id": 0})
        return list(languages)

    def getUserLearningLanguage(self, user_ID):
        """Returns a string representing the language that a user is learning"""
        if not self.doesUserExistByID(user_ID):
            return None
        res = self.user_collection.find_one(
            {"_id": ObjectId(user_ID)},
            {"learning_language": 1, '_id': 0}
        )
        return res["learning_language"]

    def setUserLearningLanguage(self, user_ID, language):
        """Sets the learning language of a user.
           Returns True if it succeeds, else false"""
        if self.doesUserExistByID(user_ID):
            self.user_collection.update(
                {"_id": ObjectId(user_ID)},
                {"$set": {"learning_language": language}}
            )
            return True
        return False


if __name__ == '__main__':
    pass
    with open('../data/data_ok.json', 'r') as f:
        data = json.load(f)

    for record in data:
        record["fr"]["nbSuccess"] = 0
        record["en"]["nbSuccess"] = 0
        record["de"]["nbSuccess"] = 0
        record["es"]["nbSuccess"] = 0
        record["fr"]["nbFailures"] = 0
        record["en"]["nbFailures"] = 0
        record["de"]["nbFailures"] = 0
        record["es"]["nbFailures"] = 0

    with open('data_ok.json', 'w', encoding='utf8') as fp:
        json.dump(data, fp, ensure_ascii=False)

    fp.close()
