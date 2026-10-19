import base64
import json

import pytest

import lambda_function


@pytest.fixture(autouse=True)
def data_path(tmp_path, monkeypatch):
    """ゲームデータの保存先をテストごとの一時ディレクトリへ差し替えます。"""
    path = tmp_path / "data.json"
    monkeypatch.setattr(lambda_function, "DATA_PATH", path)
    return path


def _make_event(method: str, path: str, body=None, is_base64: bool = False) -> dict:
    """Lambda 関数 URL と同じ形の event を作ります。"""
    event = {
        "requestContext": {"http": {"method": method, "path": path}},
        "isBase64Encoded": is_base64,
    }
    if body is not None:
        raw = json.dumps(body)
        if is_base64:
            raw = base64.b64encode(raw.encode("utf-8")).decode("ascii")
        event["body"] = raw
    return event


@pytest.fixture
def make_event():
    """Lambda 関数 URL と同じ形の event を作る関数を返します。"""
    return _make_event


@pytest.fixture
def call():
    """lambda_handler を呼び出し、 statusCode と body を返します。"""

    def _call(method: str, path: str, body=None, is_base64: bool = False):
        result = lambda_function.lambda_handler(_make_event(method, path, body, is_base64), None)
        payload = json.loads(result["body"])
        assert result["statusCode"] == payload["statusCode"]
        assert result["headers"]["Content-Type"] == "application/json"
        return payload["statusCode"], payload["body"]

    return _call
