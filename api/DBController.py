from pymongo import MongoClient
from bson.objectid import ObjectId
import datetime


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

        userID = self.user_collection.find_one({"_id": ObjectId(user_ID)}, {'_id': 1})
        if userID:
            return True
        else:
            return False


    def getInterests(self, user_ID):
        """Returns a list of the user interests of a user.
           Returns None if the user doesn't exist"""
        res = self.user_collection.find_one(
            {"_id": ObjectId(user_ID)},
            {"interests": 1, '_id': 0}
        )
        if res:
            return res["interests"]
        else:
            return None

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
        trainingWords = []
        topics = self.getInterests(user_ID)
        wordsToLearn = self.decideWordsToLearn(ObjectId(user_ID), topics, size)
        for word in wordsToLearn:
            complementaryWords = self.getComplementaryWords(word["topic"], word)
            trainingWords.append({"to_learn": word, "complementary": complementaryWords})

        return trainingWords


    def getTestingWords(self, user_ID, size):
        """For now we do the same thing as for the training"""
        return self.getTrainingWords(user_ID, size)


    def updateLearnedWords(self, user_ID, results):
        #[{wordID: ..., lang: ...}]
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
                    if elem["wordID"] == result["wordID"] and elem["lang"] == result["lang"] :
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

    def updateTestedWords(self, user_ID, results):
        #[{wordID: ..., success: True, type: "written", lang: "fr"}]

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
                    if elem["wordID"] == result["wordID"] and elem["lang"] == result["lang"]:
                        print("qdz")
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
        res = self.voc_collection.aggregate([{"$sample": {"size": size}},
                                             {"$match":  {"topic": {'$in': topics}}}])
        return [word for word in res]

    def getComplementaryWords(self, topic, word_to_learn):
        """Returns a list of 3  words different than the word_to_learn"""
        complementaryWords = self.voc_collection.aggregate([{"$sample": {"size": 3}},
                                                            {"$match": {"topic": topic}},
                                                            {"$match": {'en': {'$nin': [word_to_learn["en"]]}}}])
        return [word for word in complementaryWords]


if __name__ == '__main__':
    controller = DBController()
    #print(controller.insertUser("a"))
    #print(controller.doesUserExist("a"))
    #print(controller.doesUserExistByID("5c73ed4c2344ef2a3a8e1c2c"))
    #print(controller.setInterests("5c73ed4c2344ef2a3a8e1c2c", ["animals"]))
    #print(controller.getInterests("5c73ed4c2344ef2a3a8e1c2c"))
    #print(controller.getTrainingWords("5c73ed4c2344ef2a3a8e1c2c", 3))
    #print(controller.getTestingWords("5c73ed4c2344ef2a3a8e1c2c", 3))
    print(controller.updateLearnedWords("5c73ed4c2344ef2a3a8e1c2c", [{"wordID": "5c73ed4c2344ef2a3a8e1c2d", "lang": "fr"}]))
    controller.updateTestedWords("5c73ed4c2344ef2a3a8e1c2c", [{"wordID": "5c73ed4c2344ef2a3a8e1c2f", "success": True, "type": "written", "lang": "fr"}])

    #print(controller.getPreviousTestResults("5c73ed4c2344ef2a3a8e1c2c", "fr"))
