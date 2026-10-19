"""
Flask を通じて lambda_function.py を呼び出すモジュールです。
flask --app local_test run --port 8000
NOTE: ローカル開発環境で lambda_function.py をテストするために用意しました。
    HTTP リクエストを Lambda 関数 URL と同じ形の event にして lambda_handler へ渡します。
    そのため、ローカルと Lambda で同じ処理を通ります。
"""

from flask import Flask, Response, request
from flask_cors import CORS

import lambda_function

app = Flask(__name__)
CORS(app)


@app.route("/", defaults={"path": ""}, methods=["GET", "POST", "PUT", "PATCH", "DELETE"])
@app.route("/<path:path>", methods=["GET", "POST", "PUT", "PATCH", "DELETE"])
def proxy(path: str) -> Response:
    """
    すべてのパスのリクエストを lambda_handler へ渡します。
    """
    event = {
        "requestContext": {"http": {"method": request.method, "path": request.path}},
        "body": request.get_data(as_text=True),
        "isBase64Encoded": False,
    }
    result = lambda_function.lambda_handler(event, None)
    return Response(result["body"], status=result["statusCode"], headers=result["headers"])


# NOTE: python local_test.py でも起動できます。
if __name__ == "__main__":
    app.run(port=8000)
