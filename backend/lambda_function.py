import base64
import json
import tempfile
from datetime import UTC, datetime
from pathlib import Path
from random import sample

# NOTE: Lambda では /tmp 以外に書き込めないため、一時ディレクトリに保存します。
DATA_PATH = Path(tempfile.gettempdir()) / "the-my-mind-data.json"


def lambda_handler(event: dict, context) -> dict:
    """
    event の中身はこれ↓
        https://docs.aws.amazon.com/ja_jp/lambda/latest/dg/urls-invocation.html#urls-payloads
    context の中身はこれ↓
        https://docs.aws.amazon.com/ja_jp/lambda/latest/dg/python-context.html
    """
    HTTP_METHOD: str = event["requestContext"]["http"]["method"]
    HTTP_PATH: str = event["requestContext"]["http"]["path"]
    ROUTE_MAPS = {
        ("GET", "/"): health,
        ("POST", "/init"): init,
        ("POST", "/numbers"): numbers,
        ("POST", "/number"): number,
    }
    function = ROUTE_MAPS.get((HTTP_METHOD, HTTP_PATH))
    if not function:
        return make_response(404, {"message": "not found"})
    # 壊れた JSON や数字でない値は、 500 ではなく 400 を返します。
    try:
        result = function(parse_body(event))
    except ValueError, TypeError:
        return make_response(400, {"message": "リクエストの形式が正しくありません。"})
    return make_response(result.get("statusCode", 200), result.get("body", {}))


def parse_body(event: dict) -> dict:
    """
    関数 URL の body は JSON 文字列です。 base64 エンコードされている場合や、ない場合もあります。
    """
    body = event.get("body")
    if not body:
        return {}
    if event.get("isBase64Encoded"):
        body = base64.b64decode(body).decode("utf-8")
    return json.loads(body)


def make_response(status_code: int, body: dict) -> dict:
    """
    関数 URL のレスポンスを作ります。
    フロントエンドは response.data.statusCode と response.data.body を読むため、 body にも statusCode を含めます。
    """
    return {
        "statusCode": status_code,
        "headers": {"Content-Type": "application/json"},
        "body": json.dumps({"statusCode": status_code, "body": body}, ensure_ascii=False),
    }


def load_data() -> dict | None:
    """
    保存したデータを読み込みます。まだ初期化されていなければ None を返します。
    """
    if not DATA_PATH.exists():
        return None
    return json.loads(DATA_PATH.read_text(encoding="utf8"))


def save_data(data: dict) -> None:
    """
    データを保存します。
    """
    data["updated_at"] = datetime.now(tz=UTC).isoformat(timespec="seconds")
    DATA_PATH.write_text(json.dumps(data), encoding="utf8")


def is_game_clear(data: dict) -> bool:
    """
    ゲームオーバーにならず、配った数字をすべて出し切ったらクリアです。
    """
    return not data["game_set"] and set(data["numbers_dealed"]) <= set(data["numbers_out"])


NOT_INITIALIZED = {
    "statusCode": 400,
    "body": {"message": "まだ初期化されていません。先に初期化してください。"},
}


def health(post_data: dict) -> dict:
    return {"statusCode": 200, "body": {"message": "OK"}}


def init(post_data: dict) -> dict:
    """
    データを初期化します。
    """
    save_data(
        {
            "numbers_out": [],
            "numbers_dealed": [],
            "game_set": False,
        }
    )
    return {
        "statusCode": 200,
        "body": {"message": "初期化しました。さあカードを数字をとりましょう。"},
    }


def numbers(post_data: dict) -> dict:
    """
    1~100から数字を配布します。
    """
    how_many = int(post_data.get("how_many", 3))
    data = load_data()
    if data is None:
        return NOT_INITIALIZED
    numbers_remain = list(set(range(1, 101)) - set(data["numbers_dealed"]))
    # 求められた個数を選び出せるか?
    if len(numbers_remain) < how_many:
        return {
            "statusCode": 400,
            "body": {"message": f"残っている数字は {len(numbers_remain)} 個だけです。"},
        }
    # 選び出す。
    samples = sample(numbers_remain, how_many)
    # 保存する。
    data["numbers_dealed"] = data["numbers_dealed"] + samples
    save_data(data)
    return {
        "statusCode": 200,
        "body": {
            "message": "数字をとりました。みんなで、せーので、数字を出していきましょう。",
            "numbers": samples,
        },
    }


def number(post_data: dict) -> dict:
    """
    数字を出します。 The mind のルールに従って、エラーを出します。
    """
    # post_data["number"] を検証。
    if not post_data.get("number"):
        return {
            "statusCode": 400,
            "body": {"message": "Parameter 'number' is required"},
        }
    number = int(post_data.get("number"))
    data = load_data()
    if data is None:
        return NOT_INITIALIZED
    # 配っていない数字を出してくるんじゃねえ。
    if number not in data["numbers_dealed"]:
        return {
            "statusCode": 400,
            "body": {"message": f"'{number}' was not dealed"},
        }
    # 同じ数字を出してくるんじゃねえ。
    if number in data["numbers_out"]:
        return {
            "statusCode": 409,
            "body": {
                "message": f"'{number}' は、もう出されているよ。",
                "numbers_out": data["numbers_out"],
                "game_set": data["game_set"],
                "game_clear": is_game_clear(data),
            },
        }
    numbers_out = data["numbers_out"]
    data["numbers_out"] = numbers_out + [number]
    # The mind のルール: すでに out した数字より大きな数のみ出せる。
    if numbers_out and number < max(numbers_out):
        data["game_set"] = True
        save_data(data)
        return {
            "statusCode": 200,
            "body": {
                "message": f"'{number}' を出すことは不可能です。 '{max(numbers_out)}' がすでに出されているから。",
                "numbers_out": data["numbers_out"],
                "game_set": data["game_set"],
                "game_clear": is_game_clear(data),
            },
        }
    save_data(data)
    game_clear = is_game_clear(data)
    return {
        "statusCode": 200,
        "body": {
            "message": "全部出し切りました。クリアです!" if game_clear else "OK",
            "numbers_out": data["numbers_out"],
            "game_set": data["game_set"],
            "game_clear": game_clear,
        },
    }
