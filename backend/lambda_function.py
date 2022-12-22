import json
from datetime import datetime, timezone

# NOTE: lambda 環境には存在する。
from awslambdaric.lambda_context import LambdaContext


UTC = timezone.utc


def lambda_handler(event: dict, context: LambdaContext):
    """
    event の中身はこれ↓
        https://docs.aws.amazon.com/ja_jp/lambda/latest/dg/urls-invocation.html#urls-payloads
    context の中身はこれ↓
        https://docs.aws.amazon.com/ja_jp/lambda/latest/dg/python-context.html
    """
    HTTP_METHOD: str = event["requestContext"]["http"]["method"]
    HTTP_PATH: str = event["requestContext"]["http"]["path"]
    BODY = event["body"]
    print(type(BODY), BODY)
    ROUTE_MAPS = {
        ("GET", "/"): health,
        ("POST", "/init"): init,
        ("POST", "/numbers"): numbers,
        ("POST", "/number"): number,
    }
    function = ROUTE_MAPS.get((HTTP_METHOD, HTTP_PATH))
    if not function:
        return {
            "statusCode": 404,
            "body": "not found",
        }
    result = function(BODY)
    return {
        "statusCode": 200,
        "body": json.dumps(result)
    }


def health() -> dict:
    return {"message": "OK"}


def init() -> dict:
    """
    データを初期化します。
    """
    init_data = {
        "updated_at": datetime.now(tz=UTC).isoformat(timespec='seconds'),
        "number_out": [],
    }
    jsonized: str = json.dumps(init_data)
    with open("data.json", "w", encoding="utf8") as f:
        f.write(jsonized)
    return {"message": "OK"}


def numbers(data: dict) -> dict:
    print("numbers")
    return {}


def number(data: dict) -> dict:
    print("number")
    return {}
