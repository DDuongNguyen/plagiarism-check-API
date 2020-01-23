from flask import Flask, jsonify, request
from flask_restful import Api, Resource
from pymongo import MongoClient
import bcrypt
import pdb
import spacy


app = Flask(__name__)
api = Api(app)

client = MongoClient('mongodb://db:27017')
# client = MongoClient('mongodb://localhost:27017')
db = client.SimilarityDB
users = db.Users


def UserExist(username):
    return False if users.find({"Username": username}).count() == 0 else True


def verifyPassword(username, password):
    if not UserExist(username):
        # breakpoint()
        return False
    hashed_pw = users.find({'Username': username})[0]['Password']
    if bcrypt.checkpw(password.encode('UTF8'), hashed_pw):
        # breakpoint()
        return True
    else:
        # breakpoint()
        return False


def countTokens(username):
    tokens = users.find({'Username': username})[0]['Tokens']
    return tokens


class Register(Resource):
    def post(self):
        data = request.get_json()
        username = data['username']
        password = data['password']

        if UserExist(username):
            retJson = {
                "msg": 'yo someone already made this account'
            }
            return jsonify(retJson)

        hashed_pw = bcrypt.hashpw(password.encode('utf8'), bcrypt.gensalt())
        users.insert({
            "Username": username,
            "Password": hashed_pw,
            "Tokens": 5
        })
        retJson = {
            "message": "sucesfully created your user",
            "Username": username,
            "Password": str(hashed_pw),
            "Tokens": 5
        }
        return jsonify(retJson)


class Detection(Resource):
    def post(self):
        data = request.get_json()
        username = data['username']
        password = data['password']
        text1 = data['text1']
        text2 = data['text2']

        # validate correct user
        if not UserExist(username):
            retJson = {
                'message': 'wrong username'
            }
            return jsonify(retJson)

        # validate correct password
        if not verifyPassword(username, password):
            retJson = {
                'message': 'invalid password'
            }
            return jsonify(retJson)

        # validate enough tokens
        num_token = countTokens(username)
        if num_token <= 0:
            retJson = {
                "message": "yo refill."
            }
            return jsonify(retJson)

        # do a calculate edit distance
        nlp = spacy.load('en_core_web_sm')
        text1 = nlp(text1)
        text2 = nlp(text2)
        ratio = text1.similarity(text2)
        retJson = {
            'message': 'successfully took yo money',
            'similarity_ ratio': ratio,
            'remaining_tokens': num_token
        }

        current_tokens = countTokens(username)
        users.update({
            'Username': username
        }, {
            '$set': {
                'Tokens': current_tokens-1
            }
        })

        return jsonify(retJson)


class Refill(Resource):
    def post(self):
        data = request.get_json()
        username = data['username']
        password = data['admin_password']
        refill_amount = data['refill_amount']
        # verify user
        if not UserExist(username):
            retJson = {
                'message': 'wrong username'
            }
            return jsonify(retJson)
        # verify admin password
        admin_password = 'meow'
        if not password == admin_password:
            retJson = {
                'message': 'wrong admin password mang'
            }
            return jsonify(retJson)
        # update refill
        current_tokens = countTokens(username)
        users.update({
            'Username': username
        }, {
            '$set': {
                'Tokens': current_tokens + refill_amount
            }
        })
        retJson = {
            'message': 'you updated your tokens dough',
            'current_token': current_tokens + refill_amount,
        }
        return jsonify(retJson)


api.add_resource(Register, '/register')
api.add_resource(Refill, '/refill')
api.add_resource(Detection, '/detection')

if __name__ == '__main__':
    app.run(host='0.0.0.0')
