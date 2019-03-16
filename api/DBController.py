from pymongo import MongoClient
from bson.objectid import ObjectId
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
            query = {"email": user_email, "learning_language": language_to_learn,  "interests": [], "taughtWords": [], "testedWords": []}
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

    def getTrainingWords(self, user_ID, size):
        """Returns all the words needed for the training part
        Format: [{'to learn': word, 'complementary': [list of 3 words]}, {...}]"""
        if not self.doesUserExistByID(user_ID):
            return None

        trainingWords = {"words": []}
        topics = self.getInterests(user_ID)

        # if the user has no preferences, he will get training words from all the possible topics
        if len(topics) == 0: topics = ["animals", "food", "clothes", "colours"]

        wordsToLearn = self.decideWordsToLearn(ObjectId(user_ID), topics, size)
        for word in wordsToLearn:
            complementaryWords = self.getComplementaryWords(word["topic"], word)
            trainingWords["words"].append({"to_learn": word, "complementary": complementaryWords})

        return json.loads(JSONEncoder().encode(trainingWords))


    def getTestingWords(self, user_ID, size):
        """For now we do the same thing as for the training and we add a fied "typ" to define
        which type of test will be used for each word"""

        testingWords = {"words": []}
        if not self.doesUserExistByID(user_ID):
            return None

        topics = self.getInterests(user_ID)
        # if the user has no preferences, he will get training words from all the possible topics
        if len(topics) == 0: topics = ["animals", "food", "clothes", "colours"]

        wordsToTest = self.decideWordsToTest(user_ID, topics, size)

        for word in wordsToTest:
            complementaryWords = self.getComplementaryWords(word["topic"], word)
            testingWords["words"].append({"to_learn": word, "complementary": complementaryWords, "type": random.choice(["written", "visual"])})
        return json.loads(JSONEncoder().encode(testingWords))


    def updateLearnedWords(self, user_ID, results):
        #[{wordID: ..., lang: ...}]
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
                    if elem["wordID"] == ObjectId(result["wordID"]) and elem["lang"] == result["lang"] :
                        self.user_collection.update({"_id": ObjectId(user_ID), "taughtWords.wordID": ObjectId(result["wordID"]),
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
        #[{wordID: ..., success: True, type: "written", lang: "fr"}]
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
                        self.user_collection.update({"_id": ObjectId(user_ID), "testedWords.wordID": ObjectId(result["wordID"]),
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



    def decideWordsToLearn(self, user_ID, topics, size):
        """Returns a list of words to learn """
        #get all the words that are in the topics list
        words = self.voc_collection.aggregate([{"$match":  {"topic": {'$in': topics}}}])

        res = list(words)
        res = random.sample(res, size)

        return res

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



    def decideWordsToTest(self, user_ID, topics, size):
        """Returns a list of words to test """

        # Gets all the words learned by a user
        learnedWordsIDs = self.getLearnedWords(user_ID)
        learnedWords = self.voc_collection.aggregate([{"$match": {"_id": {'$in': learnedWordsIDs}}}])
        learnedWords = list(learnedWords)

        #Gets all the words that match the preferred topics
        topicsWords = self.voc_collection.aggregate([{"$match":  {"topic": {'$in': topics}}}])
        topicsWords = list(topicsWords)
        # Intersection between the words that the user has learned and the words in his preferences
        intersection = [learnedWord for learnedWord in learnedWords for topicsWord in topicsWords if learnedWord['_id']==topicsWord['_id']]
        # if the user has learned less words than the size of the test, we complete with random words
        to_add = [word for word in topicsWords if word not in intersection]
        to_add = random.sample(to_add, max(0,size - len(intersection)))

        to_test = intersection + to_add

        return random.sample(to_test, size)



    def getComplementaryWords(self, topic, word_to_learn):
        """Returns a list of 3 of the same topic of word_to_learn but  different than the word_to_learn"""
        words = self.voc_collection.aggregate([
                                            {"$match":  {"topic": topic}},
                                            {"$match": {"en": {"$nin": [word_to_learn["en"]]}}}])

        res = list(words)
        res = random.sample(res, 3)
        return res

if __name__ == '__main__':
    controller = DBController()
    #print(controller.insertUser("a"))
    #print(controller.doesUserExist("a"))
    #print(controller.doesUserExistByID("5c73ed4c2344ef2a3a8e1c2c"))
    #print(controller.setInterests("5c73ed4c2344ef2a3a8e1c2c", ["animals"]))
    #print(controller.getInterests("5c73ed4c2344ef2a3a8e1c2c"))
    #print(controller.getTestingWords("5c73ed4c2344ef2a3a8e1c2c", 5))
    #print(controller.getTestingWords("5c73ed4c2344ef2a3a8e1c2c", 3))
    #print(controller.updateLearnedWords("5c73ed4c2344ef2a3a8e1c2c", [{"wordID": "5c73ed4c2344ef2a3a8e1c2d", "lang": "fr"}]))
    #controller.updateLearnedWords("5c73ed4c2344ef2a3a8e1c2c", [{"wordID": "5c727e21bf137730b7f488f3", "lang": "fr"}])
    #controller.updateLearnedWords("5c73ed4c2344ef2a3a8e1c2c", [{"wordID": "5c727e21bf137730b7f488f4","lang": "fr"}])


    #print(controller.getPreviousTestResults("5c73ed4c2344ef2a3a8e1c2c", "fr"))

    languages = [{"lang": "fr", "display_name": "French"},
                 {"lang": "es", "display_name": "Spanish"},
                 {"lang": "de", "display_name": "German"}]

    controller.insertLanguages(languages)

    #print(controller.getLearningLanguages())
