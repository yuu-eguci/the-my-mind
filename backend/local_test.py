"""
Flask を通じて lambda_functions.py を呼び出すモジュールです。
pipenv run python local_test.py
NOTE: ローカル開発環境で lambda_function.py をテストするために用意しました。
"""

from flask import Flask, jsonify, request
from flask_cors import CORS

import lambda_function

app = Flask(__name__)
CORS(app)


@app.route("/", methods=["GET"])
def index():
    """
    For health check.

    """
    return jsonify(
        statusCode=200,
        body=lambda_function.health(),
    )


@app.route("/init", methods=["POST"])
def init():
    """
    NOTE: request.json を使うためには、 request header に content-type: application/json が必要。
    """
    result: dict = lambda_function.init()
    return jsonify(
        statusCode=result.get("statusCode", 200),
        body=result.get("body", {}),
    )


@app.route("/numbers", methods=["POST"])
def numbers():
    """
    NOTE: request.json を使うためには、 request header に content-type: application/json が必要。
    """
    print(type(request.json), request.json)
    result: dict = lambda_function.numbers(request.json)
    return jsonify(
        statusCode=result.get("statusCode", 200),
        body=result.get("body", {}),
    )


@app.route("/number", methods=["POST"])
def number():
    """
    NOTE: request.json を使うためには、 request header に content-type: application/json が必要。
    """
    print(type(request.json), request.json)
    result: dict = lambda_function.number(request.json)
    return jsonify(
        statusCode=result.get("statusCode", 200),
        body=result.get("body", {}),
    )


# NOTE: ローカル環境でのテスト用です。
if __name__ == "__main__":
    app.run(port=8000, debug=True)
