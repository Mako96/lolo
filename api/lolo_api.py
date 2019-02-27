from flask import request, url_for, jsonify, abort
from flask_api import FlaskAPI, status, exceptions
from flask_cors import CORS
import json

import mock_messages as mock
from DBController import *

app = FlaskAPI(__name__)
dbc = DBController()

CORS(app)


@app.route('/lolo/api/v1.0/user/register', methods=['POST'])
def register_user():
    if not request.json:
        abort(400)
    email = request.json["data"]["user"]["email"]
    userid = dbc.insertUser(email)
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


@app.route('/lolo/api/v1.0/<userid>/preferences', methods=['GET'])
def get_preferences(userid):
    #TODO: connect to db and get either user specific themes or list of all themes
    #DUMMY DATA FOR TESTING:
    categories = {
        "data": {
            "preferences": [
                {
                    "name": "Animals",
                    "image": "http://......",
                    "selected": 1
                },
                {
                    "name": "Colours",
                    "image": "http://......",
                    "selected": 0
                },
                {
                    "name": "Clothes",
                    "image": "http://......",
                    "selected": 0
                },
                {
                    "name": "Food",
                    "image": "http://......",
                    "selected": 1
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
        print("d")
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


@app.route('/lolo/api/v1.0/user/<userid>/learn/words/<int:number_of_words>', methods=['GET'])
def get_words_learn(userid, number_of_words):
    result = dbc.getTrainingWords(userid, number_of_words)
    #print(result)
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
    result = dbc.getTestingWords(userid, number_of_words)
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
    success = dbc.updateLearnedWords(userid, request.json["data"]["learned"])
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
    success = dbc.updateTestedWords(userid, request.json["data"]["tested"])
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


if __name__ == "__main__":
    app.run(debug=True)
