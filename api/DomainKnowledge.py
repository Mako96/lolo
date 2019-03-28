from bson.objectid import ObjectId


class DomainKnowledge:

    def __init__(self, dbController):
        self.dbController = dbController

    def updateDifficulties(self, testResults):
        print(testResults)
        """Update words difficulties based on users's results"""
        user_learning_lang = testResults[0]["lang"]  # the language the user is currently learning
        for result in testResults:
            self.updateWordDifficulty(result["wordID"], result["success"], user_learning_lang)

        print("updateDifficulties")

    def updateWordDifficulty(self, wordID, result, user_learning_lang):
        difficulty = self.getDifficulty(wordID, user_learning_lang)
        # if the user passed the test
        if result:
            reward = -0.2
        # if the user failled the test
        else:
            reward = 0.2
        new_difficulty = difficulty + reward

        # max difficulty is 10, min is 1
        if new_difficulty > 10:
            new_difficulty = 10
        if new_difficulty < 1:
            new_difficulty = 1

        self.updateDifficultyInDB(wordID, new_difficulty, user_learning_lang)
        print("updateWordDifficulty")

    def getDifficulty(self, wordID, user_learning_lang):
        difficulty = self.dbController.voc_collection.find_one(
            {"_id": ObjectId(wordID)},
        )
        print("getDifficulty")
        return difficulty[user_learning_lang]["difficulty_level"]

    def updateDifficultyInDB(self, wordID, new_difficulty, user_learning_lang):
        print(user_learning_lang)
        self.dbController.voc_collection.update(
            {"_id": ObjectId(wordID)},
            {"$set": {str(user_learning_lang) + ".difficulty_level": new_difficulty}}
        )
        print("updateDifficultyInDB")
