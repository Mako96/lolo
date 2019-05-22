from bson.objectid import ObjectId
from keras.models import model_from_yaml
from numpy import array
from math import floor 


class DomainKnowledge:

    def __init__(self, dbController):
        self.dbController = dbController

        # load YAML and create model
        yaml_file = open('model.yaml', 'r')
        loaded_model_yaml = yaml_file.read()
        yaml_file.close()
        self.loaded_model = model_from_yaml(loaded_model_yaml)
        # load weights into new model
        self.loaded_model.load_weights("model.h5")

    def getNbOfWordsPerTopics(self):
        res = self.dbController.voc_collection.aggregate([
            {"$group": {"_id": '$topic', "count": {"$sum": 1}}}
        ])
        res = list(res)
        res_ok = {}
        for elem in res:
            res_ok[elem["_id"]] = elem["count"]

        return res_ok

    def updateScores(self, testResults):
        """Update words difficulties based on users's results"""
        user_learning_lang = testResults[0]["lang"]  # the language the user is currently learning
        for result in testResults:
            self.updateWordDifficulty(result["wordID"], result["success"], user_learning_lang)
            self.updateNbOfSuccessAndFailure(result["wordID"], user_learning_lang, result["success"])

    def updateWordDifficulty(self, wordID, result, user_learning_lang):
        difficulty = self.getDifficulty(wordID, str(user_learning_lang))
        nbOfSuccess = self.getNbOfSuccess(wordID, str(user_learning_lang))
        nbOfFailures = self.getNbOfFailures(wordID, str(user_learning_lang))

        # L : TODO: get the actual word length from testResults
        word_list = self.dbController.voc_collection.aggregate([{"$match": {"_id": {'$in': learnedWordsIDs}}}])
        word = "bla"
        L = len(word)

        # P = proportion off failures and successes
        P = nbOfSuccess/nbOfFailures

        # if the user passed the test

        Xnew = array([[L,P]])
        # make a prediction
        ynew = self.loaded_model.predict(Xnew)
        score = floor(ynew[0][0])

        # max difficulty is 10, min is 1
        if score > 10:
            score = 10
        if score < 1:
            score = 1

        self.updateScoreInDb(wordID, score, user_learning_lang)

    def getDifficulty(self, wordID, user_learning_lang):
        difficulty = self.dbController.voc_collection.find_one(
            {"_id": ObjectId(wordID)},

        )
        return difficulty[user_learning_lang]["difficulty_level"]

    def updateScoreInDb(self, wordID, new_score, user_learning_lang):
        self.dbController.voc_collection.update(
            {"_id": ObjectId(wordID)},
            {"$set": {str(user_learning_lang) + ".score": new_score}}
        )

    def updateNbOfSuccessAndFailure(self, wordID, lang, success):
        if success:
            self.dbController.voc_collection.update(
                {"_id": ObjectId(wordID)},
                {"$inc": {str(lang) + ".nbFailures": 1}}
            )
        else:
            self.dbController.voc_collection.update(
                {"_id": ObjectId(wordID)},
                {"$inc": {str(lang) + ".nbSuccess": 1}}
            )

    def getNbOfSuccess(self, wordID, user_learning_lang):
        res = self.dbController.voc_collection.find_one(
            {"_id": ObjectId(wordID)},

        )

        return res[user_learning_lang]["nbSuccess"]

    def getNbOfFailures(self, wordID, user_learning_lang):
        res = self.dbController.voc_collection.find_one(
            {"_id": ObjectId(wordID)},
        )

        return res[user_learning_lang]["nbFailures"]