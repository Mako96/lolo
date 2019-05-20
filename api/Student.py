from bson.objectid import ObjectId
import datetime
from DomainKnowledge import *
from DBController import *
from collections import Counter
import json
import random
import re
import copy


class Student:

    def __init__(self, dbController):
        self.dbController = dbController
        self.domain = DomainKnowledge(self.dbController)

    def getStatistics(self, userID):
        pass

    def getPercentageOfWordsPassed(self, userID):
        topics = ["animals", "food", "clothes", "colours"]
        words = self.getPassedTestWords(userID)
        print(len(words))
        nbOfWordsPerTopics = self.domain.getNbOfWordsPerTopics()
        percentages = {topic: 0 for topic in topics}
        for word in words:
            for topic in ["animals", "food", "clothes", "colours"]:
                if word["topic"] == topic:
                    percentages[topic] += 1

        for key in percentages:
            percentages[key] = round((percentages[key] / nbOfWordsPerTopics[key]) * 100)

        return percentages

    def getListOfAllLearnedWords(self, userID):
        user_learning_lang = self.dbController.getUserLearningLanguage(userID)
        res = self.getAllLearnedWordsIDs(userID, user_learning_lang)
        res = [result["taughtWords"]["wordID"] for result in res]
        return self.getWordsFromIDs(res)

    def getPassedTestWords(self, userID):
        user_learning_lang = self.dbController.getUserLearningLanguage(userID)
        res = self.getAllPassedWordsIDs(userID, user_learning_lang)
        res = [result["testedWords"]["wordID"] for result in res]
        return self.getWordsFromIDs(res)

    def getWordsFromIDs(self, learnedWordsIDs):
        learnedWords = self.dbController.voc_collection.aggregate([{"$match": {"_id": {'$in': learnedWordsIDs}}}])
        learnedWords = list(learnedWords)
        return learnedWords

    def getListOfMostRecentLearnedWords(self, userID):
        """
        Returns the last 15 words learned by the user (if he has learned less than 20, it returns the maximum possible
        """
        user_learning_lang = self.dbController.getUserLearningLanguage(userID)
        previousLearnedWords = self.getLast15LearnedWordsIDs(userID, user_learning_lang)
        previousLearnedWords = [result["taughtWords"]["wordID"] for result in previousLearnedWords]
        return self.getWordsFromIDs(previousLearnedWords)

    def getPercentageOfTestsFailed(self, userID, topic):
        pass

    def mostFailedWords(self, userID, nb, topic):
        """returns the <nb> most failed words of a user"""
        pass

    def getUserFitness(self, userID, user_learning_lang):
        """
        Compute the user's fitness based on his previous 15 test results
        if he passes > 80 % of the tests -> fitness = "pro"
        if he passes between 40 % and 80 % of the tests -> fitness = "intermediate"
        if he passes between < 40 % the tests -> fitness = "bad"
         """
        previousTestResults = self.getLast15TestHistory(userID, user_learning_lang)
        successCounter = 0

        for res in previousTestResults:
            if res["testedWords"]["lastResult"]:
                successCounter += 1
        if len(previousTestResults) == 0:
            successRate = 0
        else:
            successRate = (successCounter / len(previousTestResults)) * 100
        if successRate >= 80:
            return "pro"
        elif 40 < successRate < 80:
            return "intermediate"
        else:
            return "bad"

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

    def updateTestWords(self, user_ID, results):
        # [{wordID: ..., lang: ...}]
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
                    if elem["wordID"] == ObjectId(result["wordID"]) and elem["lang"] == result["lang"] \
                            and elem["type"] == result["type"]:
                        if result["success"]:
                            self.dbController.user_collection.update(
                                {"_id": ObjectId(user_ID), "testedWords.wordID": ObjectId(result["wordID"]),
                                 "testedWords.lang": result["lang"], "testedWords.type": result["type"]},
                                {"$inc": {"testedWords.$.nbOfSuccess": 1},
                                 "$set": {"testedWords.$.dateLastSeen": date,
                                          "testedWords.$.lastResult": result["success"]}},
                            )
                        else:
                            self.dbController.user_collection.update(
                                {"_id": ObjectId(user_ID), "testedWords.wordID": ObjectId(result["wordID"]),
                                 "testedWords.lang": result["lang"], "testedWords.type": result["type"]},
                                {"$inc": {"testedWords.$.nbOfFailures": 1},
                                 "$set": {"testedWords.$.dateLastSeen": date,
                                          "testedWords.$.lastResult": result["success"]}},
                            )

                        found = True
                        break

            # if the list of testedWords is empty or the word is not learned yet
            if not testedWords or not found:
                if result["success"]:
                    self.dbController.user_collection.update({"_id": ObjectId(user_ID)},
                                                             {"$addToSet": {
                                                                 "testedWords": {'wordID': ObjectId(result["wordID"]),
                                                                                 'lang': result["lang"],
                                                                                 'dateLastSeen': date,
                                                                                 'nbOfFailures': 0,
                                                                                 'nbOfSuccess': 1,
                                                                                 'type': result["type"],
                                                                                 'lastResult': result["success"]
                                                                                 }}},
                                                             False,
                                                             True)

                else:
                    self.dbController.user_collection.update({"_id": ObjectId(user_ID)},
                                                             {"$addToSet": {
                                                                 "testedWords": {'wordID': ObjectId(result["wordID"]),
                                                                                 'lang': result["lang"],
                                                                                 'dateLastSeen': date,
                                                                                 'nbOfFailures': 1,
                                                                                 'nbOfSuccess': 0,
                                                                                 'type': result["type"],
                                                                                 'lastResult': result["success"]}}},
                                                             False,
                                                             True)
        # Here we update the difficulties of the words based on user's results
        self.domain.updateScores(results)

        return True

    def getLast15TestHistory(self, user_ID, lang):
        """Returns the last 15 tests result of a user """
        if not self.dbController.user_collection.find_one({"_id": ObjectId(user_ID)}, {'testedWords': 1})[
            'testedWords']:
            return []
        res = self.dbController.user_collection.aggregate([
            {"$match": {"_id": ObjectId(user_ID), 'testedWords.lang': lang}},
            {"$unwind": "$testedWords"},
            {"$match": {
                "testedWords.lang": lang,
            }},
            {"$sort": {
                "testedWords.dateLastSeen": -1
            }},
            {"$limit": 15}

        ])

        return list(res)

    def getLast15LearnedWordsIDs(self, user_ID, lang):
        """Returns the last 15 word's IDs that the user has learned"""
        res = self.dbController.user_collection.aggregate([
            {"$match": {"_id": ObjectId(user_ID), 'taughtWords.lang': lang}},
            {"$unwind": "$taughtWords"},
            {"$match": {
                "taughtWords.lang": lang,
            }},
            {"$sort": {
                "taughtWords.dateLastSeen": -1,
            }},
            {"$limit": 15}

        ])

        return list(res)

    def getAllLearnedWordsIDs(self, user_ID, lang):
        """Returns the wordIDs of the words that the user has learned"""
        res = self.dbController.user_collection.aggregate([
            {"$match": {"_id": ObjectId(user_ID), 'taughtWords.lang': lang}},
            {"$unwind": "$taughtWords"},
            {"$match": {
                "taughtWords.lang": lang,
            }},
        ])

        return list(res)

    def getAllPassedWordsIDs(self, user_ID, lang):
        """Returns the wordIDs of the words for which the user has passed at least one test"""
        res = self.dbController.user_collection.aggregate([
            {"$match": {"_id": ObjectId(user_ID)}},
            {"$unwind": "$testedWords"},
            {"$match": {
                "testedWords.lang": lang,
                'testedWords.nbOfSuccess': {'$ne': 0}
            }},
            {"$project": {"testedWords.wordID": 1, "_id": 0}}
        ])
        #to only have distinct wordIds in res
        res = list(res)
        seen = set()
        res_ok = [elem for elem in res if
                  [(elem["testedWords"]["wordID"]) not in seen, seen.add(elem["testedWords"]["wordID"])][0]]
        return list(res_ok)

    def getAllFailedWordsIDs(self, user_ID, lang):
        """Returns the wordIDs of the words for which the user FAILED on tests"""
        res = self.dbController.user_collection.aggregate([
            {"$match": {"_id": ObjectId(user_ID)}},
            {"$unwind": "$testedWords"},
            {"$match": {
                "testedWords.lang": lang,
                'testedWords.nbOfSuccess': {'$eq': 0}
            }},
            {"$project": {"testedWords.wordID": 1, "_id": 0}}
        ])
        #to only have distinct wordIds in res
        res = list(res)
        seen = set()
        res_ok = [elem for elem in res if
                  [(elem["testedWords"]["wordID"]) not in seen, seen.add(elem["testedWords"]["wordID"])][0]]
        return list(res_ok)


if __name__ == '__main__':
    db = DBController()
    sd = Student(db)
    print(sd.getPercentageOfWordsPassed("5c9d3e6b2344ef4d810419e9"))
