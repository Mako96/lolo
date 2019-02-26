from flask import request, url_for, jsonify, abort
from flask_api import FlaskAPI, status, exceptions
from flask_cors import CORS

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
                    "userid": userid
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


@app.route('/lolo/api/v1.0/<userid>/preferences', methods=['POST'])
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


@app.route('/lolo/api/v1.0/user/<userid>/preferences', methods=['POST'])
def set_user_preferences(userid):
    if not request.json or not 'data' in request.json:
        abort(400)
    print(userid)
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


@app.route('/lolo/api/v1.0/user/<userid>/learn/words', methods=['GET'])
def get_words_learn(userid):
    result = dbc.getTrainingWords(userid, 10)
    if result:
        return result
    else:
        return jsonify(
            {
                "error": {
                    "code": "failed",
                    "message": "Something went wrong in get_words_learn" + str(userid)
                }
            })


@app.route('/lolo/api/v1.0/user/<userid>/test/words', methods=['GET'])
def get_words_test(userid):
    result = dbc.getTestingWords(userid, 10)
    if result:
        return result
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
