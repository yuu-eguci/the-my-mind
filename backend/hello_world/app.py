import json

import awsgi
from flask import Flask

app = Flask(__name__)

@app.route('/')
def index():
    """
    For health check.

    """
    return {
        "statusCode": 200,
        "body": json.dumps({
            "message": "OK",
        }),
    }

@app.route('/init', methods=['POST'])
def init():
    return {
        "statusCode": 200,
        "body": json.dumps({
            "message": "init",
        }),
    }

@app.route('/numbers', methods=['POST'])
def numbers():
    return {
        "statusCode": 200,
        "body": json.dumps({
            "message": "numbers",
        }),
    }

@app.route('/number', methods=['POST'])
def number():
    return {
        "statusCode": 200,
        "body": json.dumps({
            "message": "number",
        }),
    }

def lambda_handler(event, context):
    return awsgi.response(app, event, context)


# NOTE: ローカル環境でのテスト用です。
if __name__ == "__main__":
    app.run(port=8000, debug=True)
