from bson.objectid import ObjectId
from collections import Counter
import json
import random


class JSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        return json.JSONEncoder.default(self, o)


class Teacher:

    def __init__(self, dbController):
        self.dbController = dbController

    # -------------------------------------TEACHING ---------------------------------------------------------------
    def getTrainingWords(self, user_ID, size):
        """Returns all the words needed for the training part
        Format: [{'to learn': word, 'complementary': [list of 3 words]}, {...}]"""
        if not self.dbController.doesUserExistByID(user_ID):
            return None

        trainingWords = {"words": []}
        topics = self.dbController.getInterests(user_ID)

        # if the user has no preferences, he will get training words from all the possible topics
        if len(topics) == 0: topics = ["animals", "food", "clothes", "colours"]

        wordsToLearn = self.decideWordsToLearn(ObjectId(user_ID), topics, size)
        for word in wordsToLearn:
            complementaryWords = self.getComplementaryWords(word["topic"], word)
            trainingWords["words"].append({"to_learn": word, "complementary": complementaryWords})

        return json.loads(JSONEncoder().encode(trainingWords))

    def decideWordsToLearn(self, user_ID, topics, size):
        """Returns a list of words to learn """
        # get all the words that are in the topics list
        words = self.dbController.voc_collection.aggregate([{"$match": {"topic": {'$in': topics}}}])
        words = list(words)

        learning_words = self.generate_words_set(size, words, user_ID)

        return learning_words

    # -------------------------------------TESTING ---------------------------------------------------------------

    def getTestingWords(self, user_ID, size):
        """For now we do the same thing as for the training and we add a fied "typ" to define
        which type of test will be used for each word"""

        testingWords = {"words": []}
        if not self.dbController.doesUserExistByID(user_ID):
            return None

        topics = self.dbController.getInterests(user_ID)
        # if the user has no preferences, he will get training words from all the possible topics
        if len(topics) == 0: topics = ["animals", "food", "clothes", "colours"]

        wordsToTest = self.decideWordsToTest(user_ID, topics, size)

        for word in wordsToTest:
            complementaryWords = self.getComplementaryWords(word["topic"], word)
            testingWords["words"].append(
                {"to_learn": word, "complementary": complementaryWords, "type": random.choice(["written", "visual"])})
        return json.loads(JSONEncoder().encode(testingWords))

    def decideWordsToTest(self, user_ID, topics, size):
        """Returns a list of words to test """

        # Gets all the words learned by a user
        learnedWordsIDs = self.dbController.getLearnedWords(user_ID)
        learnedWords = self.dbController.voc_collection.aggregate([{"$match": {"_id": {'$in': learnedWordsIDs}}}])
        learnedWords = list(learnedWords)

        # Gets all the words that match the preferred topics
        topicsWords = self.dbController.voc_collection.aggregate([{"$match": {"topic": {'$in': topics}}}])
        topicsWords = list(topicsWords)
        # Intersection between the words that the user has learned and the words in his preferences
        intersection = [learnedWord for learnedWord in learnedWords for topicsWord in topicsWords if
                        learnedWord['_id'] == topicsWord['_id']]
        # if the user has learned less words than the size of the test, we complete with random words
        to_add = [word for word in topicsWords if word not in intersection]
        to_add = random.sample(to_add, max(0, size - len(intersection)))

        # to_test contains all the words that the user have learned in a certain topic
        to_test = intersection + to_add

        testings_words = self.generate_words_set(size, to_test, user_ID)

        return testings_words

    # ------------------------------------------------------------------------------------------------------

    def generate_words_set(self, size, words, user_ID):
        """Generate words set based on the difficulty level of the words"""

        user_learning_lang = self.dbController.getUserLearningLanguage(user_ID)
        # First we need to get the distribution of the difficulty levels there are in "words"
        counter = dict(Counter([word["difficulty_" + user_learning_lang] for word in words]))
        distribution = {k: v / total for total in (sum(counter.values()),) for k, v in counter.items()}
        if not distribution.get(0):
            distribution[0] = 0
        if not distribution.get(1):
            distribution[1] = 0
        if not distribution.get(2):
            distribution[2] = 0
        # choose the number of easy, normal and hard words
        number_easy = int(round(distribution[0])) * size
        number_normal = int(round(distribution[1])) * size
        number_hard = size - number_easy - number_normal
        list_easy = random.sample([elem for elem in words if elem["difficulty_" + user_learning_lang] == 0],
                                  number_easy)
        list_normal = random.sample([elem for elem in words if elem["difficulty_" + user_learning_lang] == 1],
                                    number_normal)
        list_hard = random.sample([elem for elem in words if elem["difficulty_" + user_learning_lang] == 2],
                                  number_hard)

        return list_easy + list_hard + list_normal

    def getComplementaryWords(self, topic, word_to_learn):
        """Returns a list of 3 of the same topic of word_to_learn but  different than the word_to_learn"""
        words = self.dbController.voc_collection.aggregate([
            {"$match": {"topic": topic}},
            {"$match": {"en": {"$nin": [word_to_learn["en"]]}}}])

        res = list(words)
        res = random.sample(res, 3)
        return res

    def updateWordDifficultyLevel(self, wordID, lang):
        """Update the level of difficulty of word (identified by wordID) in the given language (lang argument)
         WordID is a string not an objectID"""
        pass

    def updateWordsDifficultyDistribution(self):
        """Based on the recent user result, we can update the difficulties of the test/learning sessions """
        pass
