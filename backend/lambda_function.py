import json

# NOTE: lambda 環境には存在する。
# DOC: https://docs.aws.amazon.com/ja_jp/lambda/latest/dg/python-context.html
from awslambdaric.lambda_context import LambdaContext


def lambda_handler(event: dict, context: LambdaContext):
    """
    event の中身はこれ↓
        https://docs.aws.amazon.com/ja_jp/lambda/latest/dg/urls-invocation.html#urls-payloads
    context の中身はこれ↓
        https://docs.aws.amazon.com/ja_jp/lambda/latest/dg/python-context.html
    """
    HTTP_METHOD = event["requestContext"]["http"]["method"]
    HTTP_PATH = event["requestContext"]["http"]["path"]
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
    result = function()
    return {
        "statusCode": 200,
        "body": json.dumps(result)
    }


def health() -> dict:
    return {"message": "OK"}


def init() -> dict:
    print("init")
    return {}


def numbers() -> dict:
    print("numbers")
    return {}


def number() -> dict:
    print("number")
    return {}
