from flask import request, url_for, jsonify, abort
from flask_api import FlaskAPI, status, exceptions
from flask_cors import CORS

import mock_messages as mock
from DBController import *

app = FlaskAPI(__name__)
dbc = DBController()

@app.route('/')
def test():
    return "ok"
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
                "data":{
                "message" : "Successfully registered",
                "userid": userid
                }
            })
    else:
        return jsonify(
            {
                "error":{
                "message" : "Something went wrong"
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
                "data":{
                "message" : "Successfully authenticated",
                "id" : userid
                }
            })
    else:
        return jsonify(
            {
                "error":{
                "message" : "Authentication failed"
                }
            })


@app.route('/lolo/api/v1.0/preferences', methods=['GET'])
def get_preferences():
    categories = {
        "data":{
            "preferences" : [
                {
                    "name" : "Animals", 
                    "image": "http://......"
                },
                {
                    "name" : "Colours", 
                    "image": "http://......"
                },
                {
                    "name" : "Clothes", 
                    "image": "http://......"
                },
                {
                    "name" : "Food", 
                    "image": "http://......"
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
                "data":{
                "message" : "Preferences successfully saved"
                }
            })
    else:
        return jsonify(
            {
                "error":{
                "message" : "Something went wrong"
                }
            })


@app.route('/lolo/api/v1.0/user/<userid>/learn/words', methods=['GET'])
def get_words_learn(userid):
    result = dbc.getTrainingWords(userid, 10)
    if result :
        return result
    else:
        return jsonify(
            {
                "error" : {
                    "code" : "failed",
                    "message" : "Something went wrong with the words"
                }
            })


@app.route('/lolo/api/v1.0/user/<userid>/learn/test', methods=['GET'])
def get_words_test(userid):
    result = dbc.getTestingWords(userid, 10)
    if result :
        return result
    else:
        return jsonify(
            {
                "error" : {
                    "code" : "failed",
                    "message" : "Something went wrong with the words"
                }
            })


@app.route('/lolo/api/v1.0/user/<userid>/learn/summary', methods=['POST'])
def learn_summary(userid):
    if not request.json :
        abort(400)
    dbc.updateLearnedWords(userid, request.json["data"]["summary"])
    return jsonify(**mock.learn_summary_message)


@app.route('/lolo/api/v1.0/user/<userid>/test/summary', methods=['POST'])
def updateTestedWords(userid):
    if not request.json :
        abort(400)
    dbc.updateLearnedWords(userid, request.json["data"]["summary"])
    return jsonify(**mock.test_summary_message)


if __name__ == "__main__":
    app.run(debug=True)
