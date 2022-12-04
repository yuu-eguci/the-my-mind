import awsgi
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route("/", methods=["GET"])
def index():
    """
    For health check.

    """
    return jsonify(
        statusCode=200,
        body={
            "message": "OK"
        }
    )

@app.route("/init", methods=["POST"])
def init():
    return jsonify(
        statusCode=200,
        body={
            "message": "init"
        }
    )

@app.route("/numbers", methods=["POST"])
def numbers():
    return jsonify(
        statusCode=200,
        body={
            "message": "numbers"
        }
    )

@app.route("/number", methods=["POST"])
def number():
    return jsonify(
        statusCode=200,
        body={
            "message": "number"
        }
    )

def lambda_handler(event, context):
    return awsgi.response(app, event, context)


# NOTE: ローカル環境でのテスト用です。
if __name__ == "__main__":
    app.run(port=8000, debug=True)
