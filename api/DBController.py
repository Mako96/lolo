from pymongo import MongoClient
from bson.objectid import ObjectId
from collections import Counter
from itertools import chain
import datetime
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
        # TODO it should also add a new field "difficulty_lang" for all the new lang in all the words documents

    def insertDifficultyLevels(self):
        """Insert 3 new fields in each word document, difficulty_fr, difficulty_en,
        difficulty_en and set them to 0. This function is used to build the db"""
        for lang in self.getLearningLanguages():
            self.voc_collection.update(
                {},
                {"$set": {"difficulty_" + lang["lang"]: 0}},
                upsert=False,
                multi=True
            )


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

    def updateLearnedWords(self, user_ID, results):
        # [{wordID: ..., lang: ...}]
        if not self.doesUserExistByID(user_ID):
            return False

        date = datetime.datetime.utcnow()

        taughtWords = self.user_collection.find_one(
            {"_id": ObjectId(user_ID)},
            {"taughtWords": 1, '_id': 0}
        )

        taughtWords = taughtWords["taughtWords"]

        found = False
        for result in results:
            if taughtWords:
                for elem in taughtWords:
                    if elem["wordID"] == ObjectId(result["wordID"]) and elem["lang"] == result["lang"]:
                        self.user_collection.update(
                            {"_id": ObjectId(user_ID), "taughtWords.wordID": ObjectId(result["wordID"]),
                             "taughtWords.lang": result["lang"]},
                            {"$inc": {"taughtWords.$.numberOfTimesSeen": 1},
                             "$set": {"taughtWords.$.dateLastSeen": date}},
                            False,
                            True)
                        found = True
                        break

            # if the list of taughtWords is empty or the word is not learned yet
            if not taughtWords or not found:
                self.user_collection.update({"_id": ObjectId(user_ID)},
                                            {"$addToSet": {"taughtWords": {'wordID': ObjectId(result["wordID"]),
                                                                           'lang': result["lang"],
                                                                           'numberOfTimesSeen': 1,
                                                                           'dateLastSeen': date}}},
                                            False,
                                            True)
        return True

    def updateTestedWords(self, user_ID, results):
        # [{wordID: ..., success: True, type: "written", lang: "fr"}]
        if not self.doesUserExistByID(user_ID):
            return False

        date = datetime.datetime.utcnow()

        testedWords = self.user_collection.find_one(
            {"_id": ObjectId(user_ID)},
            {"testedWords": 1, '_id': 0}
        )

        testedWords = testedWords["testedWords"]

        found = False
        for result in results:
            if testedWords:
                for elem in testedWords:
                    if elem["wordID"] == ObjectId(result["wordID"]) and elem["lang"] == result["lang"]:
                        self.user_collection.update(
                            {"_id": ObjectId(user_ID), "testedWords.wordID": ObjectId(result["wordID"]),
                             "testedWords.lang": result["lang"]},
                            {"$push": {
                                "testedWords.$.result":
                                    {
                                        'date': date,
                                        'success': result["success"],
                                        'type': result["type"]
                                    }
                            }})
                        found = True
                        break

            # if the list of testedWords is empty or the word is not tested yet
            if not testedWords or not found:
                self.user_collection.update({"_id": ObjectId(user_ID)},
                                            {"$addToSet": {"testedWords": {'wordID': ObjectId(result["wordID"]),
                                                                           'lang': result["lang"],
                                                                           'result': [
                                                                               {
                                                                                   'date': date,
                                                                                   'success': result["success"],
                                                                                   'type': result["type"]
                                                                               }
                                                                           ]}}})
        return True

    def getLearnedWords(self, user_ID):
        """Returns the wordIDs of the words that the user has learned"""
        learning_language = self.getUserLearningLanguage(user_ID)
        learnedWords = self.user_collection.find_one(
            {"_id": ObjectId(user_ID), "taughtWords.lang": learning_language},
            {"taughtWords.wordID": 1, '_id': 0}
        )
        if learnedWords:
            return [wordID["wordID"] for wordID in learnedWords["taughtWords"]]
        else:
            return []

    def getPreviousTestResults(self, user_ID, lang):
        """Returns a list of all the tested words of a user"""
        testResults = self.user_collection.find_one(
            {"_id": ObjectId(user_ID), "testedWords.lang": lang},
            {"testedWords": 1, '_id': 0}
        )
        if testResults:
            return testResults["testedWords"]
        else:
            return []


if __name__ == '__main__':
    controller = DBController()
    # print(controller.insertUser("a"))
    # print(controller.doesUserExist("a"))
    # print(controller.doesUserExistByID("5c73ed4c2344ef2a3a8e1c2c"))
    # print(controller.setInterests("5c73ed4c2344ef2a3a8e1c2c", ["animals"]))
    # print(controller.getInterests("5c73ed4c2344ef2a3a8e1c2c"))
    # print(controller.getTestingWords("5c73ed4c2344ef2a3a8e1c2c", 5))
    # print(controller.getTestingWords("5c73ed4c2344ef2a3a8e1c2c", 3))
    # print(controller.updateLearnedWords("5c73ed4c2344ef2a3a8e1c2c", [{"wordID": "5c73ed4c2344ef2a3a8e1c2d", "lang": "fr"}]))
    # controller.updateLearnedWords("5c73ed4c2344ef2a3a8e1c2c", [{"wordID": "5c727e21bf137730b7f488f3", "lang": "fr"}])
    # controller.updateLearnedWords("5c73ed4c2344ef2a3a8e1c2c", [{"wordID": "5c727e21bf137730b7f488f4","lang": "fr"}])

    # print(controller.getPreviousTestResults("5c73ed4c2344ef2a3a8e1c2c", "fr"))

    # languages = [{"lang": "fr", "display_name": "French"},
    #              {"lang": "es", "display_name": "Spanish"},
    #              {"lang": "de", "display_name": "German"}]

    print(controller.getTestingWords("5c8d40802344ef44b1274c0f", 5))
