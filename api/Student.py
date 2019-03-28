from bson.objectid import ObjectId
import datetime
from DomainKnowledge import *
from collections import Counter
import json
import random
import re
import copy


class Student:

    def __init__(self, dbController):
        self.dbController = dbController
        self.domain = DomainKnowledge(self.dbController)

    def updateLearnedWords(self, user_ID, results):
        # [{wordID: ..., lang: ...}]
        if not self.dbController.doesUserExistByID(user_ID):
            return False

        date = datetime.datetime.utcnow()

        taughtWords = self.dbController.user_collection.find_one(
            {"_id": ObjectId(user_ID)},
            {"taughtWords": 1, '_id': 0}
        )

        taughtWords = taughtWords["taughtWords"]

        found = False
        for result in results:
            if taughtWords:
                for elem in taughtWords:
                    if elem["wordID"] == ObjectId(result["wordID"]) and elem["lang"] == result["lang"]:
                        self.dbController.user_collection.update(
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
                self.dbController.user_collection.update({"_id": ObjectId(user_ID)},
                                                         {"$addToSet": {
                                                             "taughtWords": {'wordID': ObjectId(result["wordID"]),
                                                                             'lang': result["lang"],
                                                                             'numberOfTimesSeen': 1,
                                                                             'dateLastSeen': date}}},
                                                         False,
                                                         True)
        return True

    def updateTestedWords(self, user_ID, results):
        # [{wordID: ..., success: True, type: "written", lang: "fr"}]
        if not self.dbController.doesUserExistByID(user_ID):
            return False

        date = datetime.datetime.utcnow()

        testedWords = self.dbController.user_collection.find_one(
            {"_id": ObjectId(user_ID)},
            {"testedWords": 1, '_id': 0}
        )

        testedWords = testedWords["testedWords"]

        found = False
        for result in results:
            if testedWords:
                for elem in testedWords:
                    if elem["wordID"] == ObjectId(result["wordID"]) and elem["lang"] == result["lang"]:
                        self.dbController.user_collection.update(
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
                self.dbController.user_collection.update({"_id": ObjectId(user_ID)},
                                                         {"$addToSet": {
                                                             "testedWords": {'wordID': ObjectId(result["wordID"]),
                                                                             'lang': result["lang"],
                                                                             'result': [
                                                                                 {
                                                                                     'date': date,
                                                                                     'success': result["success"],
                                                                                     'type': result["type"]
                                                                                 }
                                                                             ]}}})


            # Here we update the difficulties of the words based on user results

        self.domain.updateDifficulties(results)


        return True

    def getPreviousTestResults(self, user_ID, lang):
        """Returns a list of all the tested words of a user"""
        testResults = self.dbController.user_collection.find_one(
            {"_id": ObjectId(user_ID), "testedWords.lang": lang},
            {"testedWords": 1, '_id': 0}
        )
        if testResults:
            return testResults["testedWords"]
        else:
            return []
