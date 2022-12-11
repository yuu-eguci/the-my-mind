"""
Flask を通じて lambda_functions.py を呼び出すモジュールです。
pipenv run python local_test.py
NOTE: ローカル開発環境で lambda_function.py をテストするために用意しました。
"""

from flask import Flask, jsonify

from lambda_function import (
    health,
    init,
    numbers,
    number,
)

app = Flask(__name__)


@app.route("/", methods=["GET"])
def index():
    """
    For health check.

    """
    return jsonify(
        statusCode=200,
        body=health(),
    )


@app.route("/init", methods=["POST"])
def init():
    return jsonify(
        statusCode=200,
        body=init(),
    )


@app.route("/numbers", methods=["POST"])
def numbers():
    return jsonify(
        statusCode=200,
        body=numbers(),
    )


@app.route("/number", methods=["POST"])
def number():
    return jsonify(
        statusCode=200,
        body=number(),
    )


# NOTE: ローカル環境でのテスト用です。
if __name__ == "__main__":
    app.run(port=8000, debug=True)
