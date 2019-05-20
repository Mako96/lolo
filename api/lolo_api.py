from flask import request, url_for, jsonify, abort
from flask_api import FlaskAPI, status, exceptions
from flask_cors import CORS
import json

from DBController import *
from Teacher import *
from Student import *

app = FlaskAPI(__name__)
dbc = DBController()
student = Student(dbc)
teacher = Teacher(dbc, student)


CORS(app)


@app.route('/lolo/api/v1.0/user/register', methods=['POST'])
def register_user():
    if not request.json:
        abort(400)
    email = request.json["data"]["user"]["email"]
    language_to_learn = request.json["data"]["user"]["language_to_learn"]
    userid = dbc.insertUser(email, language_to_learn)
    if userid:
        return jsonify(
            {
                "data": {
                    "message": "Successfully registered",
                    "id": userid
                }
            })
    else:
        return jsonify(
            {
                "error": {
                    "message": "Something went wrong in register_user()"
                }
            })


@app.route('/lolo/api/v1.0/user/auth', methods=['POST'])
def auth_user():
    if not request.json or not 'data' in request.json:
        abort(400)
    email = request.json["data"]["user"]["email"]
    userid = dbc.doesUserExist(email)
    if userid:
        return jsonify(
            {
                "data": {
                    "message": "Successfully authenticated",
                    "id": userid
                }
            })
    else:
        return jsonify(
            {
                "error": {
                    "message": "Authentication failed"
                }
            })


@app.route('/lolo/api/v1.0/topics', methods=['GET'])
def get_topics():
    #DATA ARE HARCODED FOR NOW AS THE TOPICS ARE NOT STORED IN THE DB :
    categories = {
        "data": {
            "topics": [
                {
                    "name": "animals",
                    "image": "topics/animals.jpg",

                },
                {
                    "name": "colours",
                    "image": "topics/colours.jpg",
                },
                {
                    "name": "clothes",
                    "image": "topics/clothes.jpg",
                },
                {
                    "name": "food",
                    "image": "topics/food.jpg",
                },
            ]
        }
    }
    return jsonify(**categories)

@app.route('/lolo/api/v1.0/user/<userid>/preferences', methods=['GET'])
def get_user_preferences(userid):
    result = dbc.getInterests(userid)
    if result is not None:
        return jsonify(
            {
                "data": {
                    "preferences": result,
                }
            })
    else:
        return jsonify(
            {
                "error": {
                    "code": "failed",
                    "message": "Something went wrong in get_user_preferences" + str(userid)
                }
            })


@app.route('/lolo/api/v1.0/user/<userid>/preferences', methods=['POST'])
def set_user_preferences(userid):
    if not request.json or not 'data' in request.json:
        abort(400)
    interests = request.json["data"]["preferences"]
    success = dbc.setInterests(userid, interests)
    if success:
        return jsonify(
            {
                "data": {
                    "message": "Preferences successfully saved"
                }
            })
    else:
        return jsonify(
            {
                "error": {
                    "message": "Something went wrong in set_user_preferences()"
                }
            })


@app.route('/lolo/api/v1.0/languages', methods=['GET'])
def get_languages():
    categories = {
        "data": {
            "languages": dbc.getLearningLanguages()
        }
    }
    return jsonify(**categories)


@app.route('/lolo/api/v1.0/user/<userid>/language_to_learn', methods=['GET'])
def get_user_language_to_learn(userid):
    result = dbc.getUserLearningLanguage(userid)
    if result is not None:
        return jsonify(
            {
                "data": {
                    "lang": result,
                }
            })
    else:
        return jsonify(
            {
                "error": {
                    "code": "failed",
                    "message": "Something went wrong in get_user_language_to_learn" + str(userid)
                }
            })

@app.route('/lolo/api/v1.0/user/<userid>/language_to_learn', methods=['POST'])
def set_user_language_to_learn(userid):
    if not request.json or not 'data' in request.json:
        abort(400)
    language_to_learn = request.json["data"]["language_to_learn"]
    success = dbc.setUserLearningLanguage(userid, language_to_learn)
    if success:
        return jsonify(
            {
                "data": {
                    "message": "language to learn successfully saved"
                }
            })
    else:
        return jsonify(
            {
                "error": {
                    "message": "Something went wrong in set_user_language_to_learn()"
                }
            })

@app.route('/lolo/api/v1.0/user/<userid>/learn/words/<int:number_of_words>', methods=['GET'])
def get_words_learn(userid, number_of_words):
    result = teacher.getTrainingWords(userid, number_of_words)
    if result:
        return json.dumps({
            "data": result
        }, ensure_ascii=False).encode('utf8')
    else:
        return jsonify(
            {
                "error": {
                    "code": "failed",
                    "message": "Something went wrong in get_words_learn" + str(userid)
                }
            })


@app.route('/lolo/api/v1.0/user/<userid>/test/words/<int:number_of_words>', methods=['GET'])
def get_words_test(userid, number_of_words):
    result = teacher.getTestingWords(userid, number_of_words)
    if result:
        return json.dumps({
                "data": result
            }, ensure_ascii=False).encode('utf8')

    else:
        return jsonify(
            {
                "error": {
                    "code": "failed",
                    "message": "Something went wrong in get_words_test" + str(userid)
                }
            })


@app.route('/lolo/api/v1.0/user/<userid>/learn/update', methods=['POST'])
def update_learning_data(userid):
    if not request.json:
        abort(400)
    success = student.updateLearnedWords(userid, request.json["data"]["learned"])
    if success:
        return jsonify(
            {
                "data": {
                    "message": "Successfully updated"
                }
            })
    else:
        return jsonify(
            {
                "error": {
                    "message": "Something went wrong in update_learning_data for user " + str(userid)
                }
            })


@app.route('/lolo/api/v1.0/user/<userid>/test/update', methods=['POST'])
def update_testing_data(userid):
    if not request.json:
        abort(400)
    success = student.updateTestWords(userid, request.json["data"]["tested"])
    if success:
        return jsonify(
            {
                "data": {
                    "message": "Successfully updated"
                }
            })
    else:
        return jsonify(
            {
                "error": {
                    "message": "Something went wrong in update_testing_data()"
                }
            })

@app.route('/lolo/api/v1.0/user/<userid>/stat', methods=['GET'])
def get_user_stats(userid):
    result = student.getPercentageOfWordsPassed(userid)
    if result is not None:
        return jsonify(
            {
                "data": {
                    "stat": result,
                }
            })
    else:
        return jsonify(
            {
                "error": {
                    "code": "failed",
                    "message": "Something went wrong in get_user_stats " + str(userid)
                }
            })

@app.route('/lolo/api/v1.0/user/<userid>/stat/words', methods=['GET'])
def get_user_stats_words(userid):
    result = student.getPassedTestWords(userid)
    if result is not None:
        return jsonify(
            {
                "data": {
                    "stat": result,
                }
            })
    else:
        return jsonify(
            {
                "error": {
                    "code": "failed",
                    "message": "Something went wrong in get_user_stats_words " + str(userid)
                }
            })

if __name__ == "__main__":
    app.run(debug=True)
