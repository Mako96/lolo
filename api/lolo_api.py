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
    if not request.json: #  or not 'data' in request.json
        abort(400)
    email = request.json["data"]["user"]["email"]
    success = dbc.insertUser(email)
    if success:
        return jsonify(
            {
                "data":{
                "message" : "Successfully registered"
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
    success = dbc.doesUserExist(email)
    if success:
        return jsonify(
            {
                "data":{
                "message" : "Successfully authenticated"
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
        },
        "error":{
            "code" : "failed"
        }
}
    return jsonify(**categories)


@app.route('/lolo/api/v1.0/user/preferences', methods=['POST'])
def set_user_preferences():
    if not request.json or not 'data' in request.json:
        abort(400)
    email = request.json["data"]["user"]["email"]
    interests = request.json["data"]["user"]["preferences"]
    success = dbc.setInterests(email, interests)
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


@app.route('/lolo/api/v1.0/user/<int:user_id>/learn/words', methods=['GET'])
def get_words_learn():
    return jsonify(**mock.learn_words_message)


@app.route('/lolo/api/v1.0/user/<int:user_id>/learn/test', methods=['GET'])
def get_words_test():
    return jsonify(**mock.test_words_message)


@app.route('/lolo/api/v1.0/user/<int:user_id>/learn/summary', methods=['POST'])
def learn_summary():
    if not request.json or not 'data' in request.json:
        abort(400)
    print(request.json)
    return jsonify(**mock.learn_summary_message)


@app.route('/lolo/api/v1.0/user/<int:user_id>/test/summary', methods=['POST'])
def test_summary():
    if not request.json or not 'data' in request.json:
        abort(400)
    print(request.json)
    return jsonify(**mock.test_summary_message)


if __name__ == "__main__":
    app.run(debug=True)
