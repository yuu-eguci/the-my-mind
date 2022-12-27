import json
from datetime import datetime, timezone
from random import sample

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
        "statusCode": result.get("statusCode", 200),
        "body": json.dumps(result.get("body", {}))
    }


def health() -> dict:
    return {
        "statusCode": 200,
        "body": {
            "message": "OK"
        }
    }


def init() -> dict:
    """
    データを初期化します。
    """
    init_data = {
        "updated_at": datetime.now(tz=UTC).isoformat(timespec="seconds"),
        "numbers_out": [],
        "numbers_distributed": [],
    }
    jsonized: str = json.dumps(init_data)
    with open("data.json", "w", encoding="utf8") as f:
        f.write(jsonized)
    return {
        "statusCode": 200,
        "body": {
            "message": "Successfully initialized"
        }
    }


def numbers(post_data: dict) -> dict:
    """
    1~100から数字を配布します。
    """
    how_many = int(post_data.get("how_many", 3))
    with open("data.json", "r", encoding="utf8") as f:
        data = json.loads(f.read())
    numbers_distributed = data.get("numbers_distributed", [])
    numbers_remain = list(set(range(1, 100)) - set(numbers_distributed))
    # 求められた個数を選び出せるか?
    if len(numbers_remain) < how_many:
        return {
            "statusCode": 400,
            "body": {
                "message": f"Only {len(numbers_remain)} numbers left"
            }
        }
    # 選び出す。
    samples = sample(numbers_remain, how_many)
    print("samples", samples)
    # 保存する。
    data["updated_at"] = datetime.now(tz=UTC).isoformat(timespec="seconds")
    data["numbers_distributed"] = data["numbers_distributed"] + samples
    jsonized: str = json.dumps(data)
    with open("data.json", "w", encoding="utf8") as f:
        f.write(jsonized)
    return {
        "statusCode": 200,
        "body": {
            "message": "OK",
            "numbers": samples,
        }
    }


def number(post_data: dict) -> dict:
    """
    数字を出します。 The mind のルールに従って、エラーを出します。
    """
    # post_data["number"] を検証。
    if not post_data.get("number"):
        return {
            "statusCode": 400,
            "body": {
                "message": "Parameter 'number' is required"
            }
        }
    number = int(post_data.get("number"))
    with open("data.json", "r", encoding="utf8") as f:
        data = json.loads(f.read())
    # 配っていない数字を出してくるんじゃねえ。
    if number not in data["numbers_distributed"]:
        return {
            "statusCode": 400,
            "body": {
                "message": f"'{number}' was not distributed"
            }
        }
    numbers_out = data.get("numbers_out", [])
    # The mind のルール: すでに out した数字より大きな数のみ出せる。
    if number < max(numbers_out):
        return {
            "statusCode": 200,
            "body": {
                "message": f"'{number}' cannot be out; '{max(numbers_out)}' is already out"
            }
        }
    data["numbers_out"].append(number)
    jsonized: str = json.dumps(data)
    with open("data.json", "w", encoding="utf8") as f:
        f.write(jsonized)
    return {
        "statusCode": 200,
        "body": {
            "message": "OK",
            "numbers_out": data["numbers_out"]
        }
    }
