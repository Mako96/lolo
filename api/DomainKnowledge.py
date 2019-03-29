from bson.objectid import ObjectId


class DomainKnowledge:

    def __init__(self, dbController):
        self.dbController = dbController

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

        # if the user passed the test

        score = difficulty + 0.2 * (nbOfSuccess - nbOfFailures)

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