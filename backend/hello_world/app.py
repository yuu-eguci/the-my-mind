import json

import awsgi
from flask import Flask

app = Flask(__name__)

@app.route('/')
def index():
    return {
        "statusCode": 200,
        "body": json.dumps({
            "message": "index",
        }),
    }

@app.route('/hello', methods=['GET'])
def hello_get():
    return {
        "statusCode": 200,
        "body": json.dumps({
            "message": "get method",
        }),
    }

@app.route('/hello', methods=['POST'])
def hello_post():
    return {
        "statusCode": 200,
        "body": json.dumps({
            "message": "post method",
        }),
    }

def lambda_handler(event, context):
    return awsgi.response(app, event, context)
