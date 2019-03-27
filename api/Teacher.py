from bson.objectid import ObjectId
from collections import Counter
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


class Teacher:

    def __init__(self, dbController):
        self.dbController = dbController

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
        """Returns a list of words to learn """
        # get all the words that are in the topics list
        words = self.dbController.voc_collection.aggregate([{"$match": {"topic": {'$in': topics}}}])
        words = list(words)

        print("hereTOLe")

        learning_words = self.generate_words_set(size, words, user_learning_lang)

        return learning_words

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

        wordsToTest = self.decideWordsToTest(user_ID, topics, size, user_learning_lang)

        for word in wordsToTest:
            # decide which test can be done for the word
            possible_tests = copy.deepcopy(TYPES_OF_TEST)
            if len(word["en"]["sentences"]) == 0: # if no sentences for this word
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



    def decideWordsToTest(self, user_ID, topics, size, user_learning_lang):
        """Returns a list of words to test """
        # Gets all the words learned by a user
        learnedWordsIDs = self.getLearnedWords(user_ID)

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

        testings_words = self.generate_words_set(size, to_test, user_learning_lang)

        return testings_words

    # ------------------------------------------------------------------------------------------------------

    def generate_words_set(self, size, words, user_learning_lang):
        """Generate words set based on the difficulty level of the words"""
        # First we need to get the distribution of the difficulty levels there are in "words"
        counter = dict(Counter([int(word[user_learning_lang]["difficulty_level"]) for word in words]))
        distribution = {k: v / total for total in (sum(counter.values()),) for k, v in counter.items()}
        for i in range(1, 11):  # 1 to 10
            if not distribution.get(i):
                distribution[i] = 0
        # choose the number of easy, normal and hard words
        number_easy = 0
        for i in range(1, 4):
            number_easy += distribution[i]
        number_normal = 0
        for i in range(4, 8):
            number_normal += distribution[i]
        number_hard = 0
        for i in range(8, 11):
            number_hard += distribution[i]

        number_easy = int(round(number_easy * size))
        number_normal = int(round(number_normal * size))
        number_hard = size - number_easy - number_normal

        list_easy = random.sample([elem for elem in words if elem[user_learning_lang]["difficulty_level"] < 4],
                                  number_easy)
        list_normal = random.sample([elem for elem in words if 4 <= elem[user_learning_lang]["difficulty_level"] <= 7],
                                    number_normal)
        list_hard = random.sample([elem for elem in words if 8 <= elem[user_learning_lang]["difficulty_level"]],
                                  number_hard)

        return list_easy + list_hard + list_normal

    def getComplementaryWords(self, topic, word_to_learn):
        """Returns a list of 3 of the same topic of word_to_learn but  different than the word_to_learn"""
        words = self.dbController.voc_collection.aggregate([
            {"$match": {"topic": topic}},
            {"$match": {"id": {"$nin": [word_to_learn["id"]]}}}])

        res = list(words)
        res = random.sample(res, 3)
        return res

    def getLearnedWords(self, user_ID):
        """Returns the wordIDs of the words that the user has learned"""
        learning_language = self.dbController.getUserLearningLanguage(user_ID)
        learnedWords = self.dbController.user_collection.find_one(
            {"_id": ObjectId(user_ID), "taughtWords.lang": learning_language},
            {"taughtWords.wordID": 1, '_id': 0}
        )
        if learnedWords:
            return [wordID["wordID"] for wordID in learnedWords["taughtWords"]]
        else:
            return []

    def updateWordDifficultyLevel(self, wordID, lang):
        """Update the level of difficulty of a word (identified by wordID) in the given language (lang argument)
         WordID is a string not an objectID"""
        pass

    def updateWordsDifficultyDistribution(self):
        """Based on the recent user result, we can update the difficulties of the test/learning sessions """
        pass
