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

    def insertUser(self, user_email):
        """ Inserts an email address in the user collection
            Returns the userID if it succeeds else None"""
        if not self.doesUserExist(user_email):
            query = {"email": user_email, "interests": [], "taughtWords": [], "testedWords": []}
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

    def getTrainingWords(self, user_ID, size):
        """Returns all the words needed for the training part
        Format: [{'to learn': word, 'complementary': [list of 3 words]}, {...}]"""
        if not self.doesUserExistByID(user_ID):
            return None
        else:
            trainingWords = {"words": []}
            topics = self.getInterests(user_ID)
            wordsToLearn = self.decideWordsToLearn(ObjectId(user_ID), topics, size)
            print(len(wordsToLearn))
            print(wordsToLearn)
            for word in wordsToLearn:
                complementaryWords = self.getComplementaryWords(word["topic"], word)
                trainingWords["words"].append({"to_learn": word, "complementary": complementaryWords})

            return json.loads(JSONEncoder().encode(trainingWords))


    def getTestingWords(self, user_ID, size):
        """For now we do the same thing as for the training and we add a fied "typ" to define
        which type of test will be used for each word"""
        testingWords = self.getTrainingWords(user_ID, size)
        for word in testingWords["words"]:
            word["type"] = random.choice(["written", "visual"])
        return testingWords


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
        res = []
        while len(res) != size:
           word = self.voc_collection.aggregate([{"$sample": {"size": 1}},
                                            {"$match":  {"topic": {'$in': topics}}}])
          
           for elem in word:
              res.append(elem)
        return res

    def getComplementaryWords(self, topic, word_to_learn):
        """Returns a list of 3  words different than the word_to_learn"""
        res = []
        while len(res) != 3:
           word = self.voc_collection.aggregate([{"$sample": {"size": 1}},
                                            {"$match":  {"topic": topic}}, 
                                            {"$match": {"en": {"$nin": [word_to_learn["en"]]}}}])
               
           for elem in word:
              res.append(elem)
        return res

if __name__ == '__main__':
    controller = DBController()
    #print(controller.insertUser("a"))
    #print(controller.doesUserExist("a"))
    #print(controller.doesUserExistByID("5c73ed4c2344ef2a3a8e1c2c"))
    #print(controller.setInterests("5c73ed4c2344ef2a3a8e1c2c", ["animals"]))
    #print(controller.getInterests("5c73ed4c2344ef2a3a8e1c2c"))
    print(controller.getTrainingWords("5c73ed4c2344ef", 3))
    #print(controller.getTestingWords("5c73ed4c2344ef2a3a8e1c2c", 3))
    #print(controller.updateLearnedWords("5c73ed4c2344ef2a3a8e1c2c", [{"wordID": "5c73ed4c2344ef2a3a8e1c2d", "lang": "fr"}]))
    #controller.updateTestedWords("5c73ed4c2344ef2a3a8e1c2c", [{"wordID": "5c73ed4c2344ef2a3a8e1c2f", "success": True, "type": "written", "lang": "fr"}])

    #print(controller.getPreviousTestResults("5c73ed4c2344ef2a3a8e1c2c", "fr"))
