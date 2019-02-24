from pymongo import MongoClient
import datetime


class DBController:

    def __init__(self):
        client = MongoClient(port=27017)
        self.db = client.loloDB
        self.user_collection = self.db["users"]
        self.voc_collection = self.db["vocabulary"]

    def insertUser(self, user_email):
        """ Inserts an email address in the user collection
            Returns true if it succeeds else false"""
        if not self.doesUserExist(user_email):
            query = {"email": user_email, "interests": [], "taughtWords": [], "testedWords": []}
            self.user_collection.insert_one(query)
            return True
        else:
            return False

    def doesUserExist(self, user_email):
        query = {"email": user_email}
        count = self.user_collection.find(query).count()
        return count == 1

    def getInterests(self, user_email):
        """Returns a list of the user interests of a user.
           Returns None if the user doesn't exist"""
        res = self.user_collection.find_one(
            {"email": user_email},
            {"interests": 1, '_id': 0}
        )
        return res["interests"]

    def setInterests(self, user_email, interests):
        """Sets the interests of a user. Takes a list of interests and the email as arguments.
           Returns True if it succeeds, else false"""
        if self.doesUserExist(user_email):
            self.user_collection.update(
                {"email": user_email},
            {"$set": {"interests": interests}}
            )
            return True
        return False

    def getTrainingWords(self, user_email, size):
        """Returns all the words needed for the training part
        Format: [{'to learn': word, 'complementary': [list of 3 words]}, {...}]"""
        trainingWords = []
        topics = self.getInterests(user_email)
        wordsToLearn = self.decideWordsToLearn(user_email, topics, size)
        for word in wordsToLearn:
            complementaryWords = self.getComplementaryWords(word["topic"], word)
            trainingWords.append({"to_learn": word, "complementary": complementaryWords})

        return trainingWords


    def getTestingWords(self, user_email, topic, size):
        """For now we do the same thing as for the training"""
        return self.getTrainingWords(user_email, topic, size)


    def updateLearnedWords(self, user_email, results):
        #[{wordID: ..., lang: ...}]
        date = datetime.datetime.utcnow()

        taughtWords = self.user_collection.find_one(
            {"email": user_email},
            {"taughtWords": 1, '_id': 0}
        )

        taughtWords = taughtWords["taughtWords"]

        found = False
        for result in results:
            if taughtWords:
                for elem in taughtWords:
                    if elem["wordID"] == result["wordID"] and elem["lang"] == result["lang"] :
                        self.user_collection.update({"email": user_email, "taughtWords.wordID": result["wordID"],
                                                    "taughtWords.lang": result["lang"]},
                                            {"$inc": {"taughtWords.$.numberOfTimesSeen": 1},
                                             "$set": {"taughtWords.$.dateLastSeen": date}},
                                             False,
                                             True)
                        found = True
                        break

            # if the list of taughtWords is empty or the word is not learned yet
            if not taughtWords or not found:
                self.user_collection.update({"email": user_email},
                                            {"$addToSet": {"taughtWords": {'wordID': result["wordID"],
                                                                           'lang': result["lang"],
                                                                           'numberOfTimesSeen': 1,
                                                                           'dateLastSeen': date}}},
                                            False,
                                            True)

    def updateTestedWords(self, user_email, results):
        #[{wordID: ..., success: True, type: "written", lang: "fr"}]

        date = datetime.datetime.utcnow()

        testedWords = self.user_collection.find_one(
            {"email": user_email},
            {"testedWords": 1, '_id': 0}
        )

        testedWords = testedWords["testedWords"]

        found = False
        for result in results:
            if testedWords:
                for elem in testedWords:
                    if elem["wordID"] == result["wordID"] and elem["lang"] == result["lang"]:
                        print("qdz")
                        self.user_collection.update({"email": user_email, "testedWords.wordID": result["wordID"],
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
                self.user_collection.update({"email": user_email},
                                            {"$addToSet": {"testedWords": {'wordID': result["wordID"],
                                                                           'lang': result["lang"],
                                                                           'result': [
                                                                               {
                                                                                'date': date,
                                                                                'success': result["success"],
                                                                                'type': result["type"]
                                                                               }
                                                                           ]}}})


    def getPreviousTestResults(self, user_email, lang):
        """Returns a list of all the tested words of a user"""
        testResults = self.user_collection.find_one(
            {"email": user_email, "testedWords.lang": lang},
            {"testedWords": 1, '_id': 0}
        )

        return testResults["testedWords"]



    def decideWordsToLearn(self, user_email, topics, size):
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
    # print(controller.setInterests("p@p.com", ["animals"]))
    # print(controller.getInterests("p@p.com"))
    #print(controller.getTrainingWords('p@p.com', 5))
    #print(controller.updateLearnedWords("p@p.com", ["5c727e21bf137730b7f411111"]))
    #controller.updateTestedWords("p@p.com", [{"wordID": 111, "success": True, "type": "written", "lang": "fr"}])
    print(controller.getPreviousTestResults("p@p.com", "fr"))