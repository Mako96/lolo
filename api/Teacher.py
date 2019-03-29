from bson.objectid import ObjectId
from collections import Counter
from DBController import *
from Student import *
import json
import random
import re
import copy


class JSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        return json.JSONEncoder.default(self, o)


TYPES_OF_TEST = ["visual", "written", "sentence", "pronunciation"]


def chooseRandomWithoutDuplicate(list, size):
    res = []
    for i in range(size):
        rand = random.randint(0, len(list) - 1)
        while list[rand] in res:
            rand = random.randint(0, len(list) - 1)
        res.append(list[rand])
    return res


class Teacher:

    def __init__(self, dbController, student):
        self.dbController = dbController
        self.student = student

    # -------------------------------------TEACHING ---------------------------------------------------------------
    def getTrainingWords(self, user_ID, size):
        """Returns all the words needed for the training part
        Format: [{'to learn': word, 'complementary': [list of 3 words]}, {...}]"""
        user_learning_lang = self.dbController.getUserLearningLanguage(user_ID)
        if not self.dbController.doesUserExistByID(user_ID):
            return None

        trainingWords = {"words": []}
        topics = self.dbController.getInterests(user_ID)

        # if the user has no preferences, he will get training words from all the possible topics
        if len(topics) == 0: topics = ["animals", "food", "clothes", "colours"]

        wordsToLearn = self.decideWordsToLearn(ObjectId(user_ID), topics, size, user_learning_lang)
        for word in wordsToLearn:
            complementaryWords = self.getComplementaryWords(word["topic"], word)
            trainingWords["words"].append({"to_learn": word, "complementary": complementaryWords})

        return json.loads(JSONEncoder().encode(trainingWords))

    def decideWordsToLearn(self, user_ID, topics, size, user_learning_lang):
        """
        Returns a list of words to learn
        The words will be chosen using the fitness of the topics and the  of the words
        the highest is the fitness the higher is the probability of having difficult words
        """

        # get all the words that are in the topics of the user
        words = self.dbController.voc_collection.aggregate([{"$match": {"topic": {'$in': topics}}}])
        words = list(words)
        # get the fitness (pro or intermediate or bad) of the user
        fitness = self.student.getUserFitness(user_ID, user_learning_lang)
        list_to_choose_from = []

        # cat1 = word_difficulty < 4 | cat2 = 4 <= word_difficulty < 8 | cat3 >= 8
        weights = {"pro": {"cat1": 1, "cat2": 2, "cat3": 3}, "intermediate": {"cat1": 1, "cat2": 2, "cat3": 1},
                   "bad": {"cat1": 3, "cat2": 1, "cat3": 1}}

        for word in words:
            if word[user_learning_lang]["score"] >= 8:
                list_to_choose_from.extend([word] * weights[fitness]["cat3"])
            elif 4 <= word[user_learning_lang]["score"] < 8:
                list_to_choose_from.extend([word] * weights[fitness]["cat2"])
            elif word[user_learning_lang]["score"] < 4:
                list_to_choose_from.extend([word] * weights[fitness]["cat1"])

        return chooseRandomWithoutDuplicate(list_to_choose_from, size)

    # -------------------------------------TESTING ---------------------------------------------------------------

    def getTestingWords(self, user_ID, size):
        """For now we do the same thing as for the training and we add a fied "typ" to define
        which type of test will be used for each word"""

        user_learning_lang = self.dbController.getUserLearningLanguage(user_ID)
        testingWords = {"words": []}

        if not self.dbController.doesUserExistByID(user_ID):
            return None

        topics = self.dbController.getInterests(user_ID)
        # if the user has no preferences, he will get training words from all the possible topics
        if len(topics) == 0: topics = ["animals", "food", "clothes", "colours"]

        wordsToTest = self.decideWordsToTest(user_ID, topics, size)

        for word in wordsToTest:
            # decide which test can be done for the word
            possible_tests = copy.deepcopy(TYPES_OF_TEST)
            if len(word["en"]["sentences"]) == 0:  # if no sentences for this word
                possible_tests.remove("sentence")
            else:
                possible_tests.remove("written")

            complementaryWords = self.getComplementaryWords(word["topic"], word)
            data = {"to_learn": word, "complementary": complementaryWords,
                    "type": random.choice(possible_tests)}
            if data["type"] == "sentence":
                data = self.setup_sentence_test(data, user_learning_lang, word)

            testingWords["words"].append(data)

        return json.loads(JSONEncoder().encode(testingWords))

    def setup_sentence_test(self, data, user_learning_lang, word):
        data["sentence_index"] = random.randint(0, len(word["en"]["sentences"]) - 1)  # choose a random sentence

        sentence = data["to_learn"][user_learning_lang]["sentences"][int(data["sentence_index"])]
        pattern = re.compile(word[user_learning_lang]["word"], re.IGNORECASE)
        sentence = pattern.sub("___", sentence)

        data["to_learn"][user_learning_lang]["sentences"][int(data["sentence_index"])] = sentence

        return data

    def decideWordsToTest(self, user_ID, topics, size):
        """Returns a list of words to test """
        # Gets all the words learned by a user
        learnedWords = self.student.getListOfMostRecentLearnedWords(user_ID)
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

        return chooseRandomWithoutDuplicate(to_test, size)

    # ------------------------------------------------------------------------------------------------------

    def getComplementaryWords(self, topic, word_to_learn):
        """Returns a list of 3 of the same topic of word_to_learn but  different than the word_to_learn"""
        words = self.dbController.voc_collection.aggregate([
            {"$match": {"topic": topic}},
            {"$match": {"id": {"$nin": [word_to_learn["id"]]}}}
        ])

        res = list(words)
        res = random.sample(res, 3)
        return res



