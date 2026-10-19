import json

import lambda_function


def test_health(call):
    assert call("GET", "/") == (200, {"message": "OK"})


def test_not_found(call):
    status, body = call("GET", "/unknown")
    assert status == 404
    assert "message" in body


def test_init_creates_empty_game(call, data_path):
    status, _ = call("POST", "/init")
    assert status == 200
    data = json.loads(data_path.read_text(encoding="utf8"))
    assert data["numbers_out"] == []
    assert data["numbers_dealed"] == []
    assert data["game_set"] is False


def test_data_path_is_under_temp_dir():
    import importlib
    import tempfile
    from pathlib import Path

    module = importlib.reload(lambda_function)
    assert Path(module.DATA_PATH).parent == Path(tempfile.gettempdir())


def test_numbers_default_is_three(call):
    call("POST", "/init")
    status, body = call("POST", "/numbers")
    assert status == 200
    assert len(body["numbers"]) == 3


def test_numbers_how_many(call):
    call("POST", "/init")
    status, body = call("POST", "/numbers", {"how_many": 5})
    assert status == 200
    assert len(body["numbers"]) == 5


def test_numbers_deals_1_to_100_without_duplicates(call):
    call("POST", "/init")
    status, body = call("POST", "/numbers", {"how_many": 100})
    assert status == 200
    assert sorted(body["numbers"]) == list(range(1, 101))


def test_numbers_not_enough_remaining(call):
    call("POST", "/init")
    call("POST", "/numbers", {"how_many": 98})
    status, body = call("POST", "/numbers", {"how_many": 3})
    assert status == 400
    assert "2" in body["message"]


def test_numbers_before_init(call):
    status, body = call("POST", "/numbers")
    assert status == 400
    assert "初期化" in body["message"]


def test_number_before_init(call):
    status, body = call("POST", "/number", {"number": 1})
    assert status == 400
    assert "初期化" in body["message"]


def test_number_missing_param(call):
    call("POST", "/init")
    status, _ = call("POST", "/number", {})
    assert status == 400


def test_number_not_dealt(call):
    call("POST", "/init")
    _, body = call("POST", "/numbers", {"how_many": 1})
    not_dealt = 1 if body["numbers"][0] != 1 else 2
    status, _ = call("POST", "/number", {"number": not_dealt})
    assert status == 400


def test_number_ascending_ok_and_duplicate_409(call):
    call("POST", "/init")
    call("POST", "/numbers", {"how_many": 100})
    assert call("POST", "/number", {"number": 10})[0] == 200
    status, body = call("POST", "/number", {"number": 20})
    assert status == 200
    assert body["numbers_out"] == [10, 20]
    assert body["game_set"] is False
    status, body = call("POST", "/number", {"number": 20})
    assert status == 409
    assert body["numbers_out"] == [10, 20]


def test_number_descending_is_game_set(call):
    call("POST", "/init")
    call("POST", "/numbers", {"how_many": 100})
    call("POST", "/number", {"number": 50})
    status, body = call("POST", "/number", {"number": 40})
    assert status == 200
    assert body["game_set"] is True


def test_body_as_base64(call):
    call("POST", "/init")
    status, body = call("POST", "/numbers", {"how_many": 4}, is_base64=True)
    assert status == 200
    assert len(body["numbers"]) == 4


def test_body_none(call, make_event):
    call("POST", "/init")
    event = make_event("POST", "/numbers")
    event["body"] = None
    result = lambda_function.lambda_handler(event, None)
    assert result["statusCode"] == 200
    assert len(json.loads(result["body"])["body"]["numbers"]) == 3


def test_response_keeps_japanese(make_event):
    event = make_event("POST", "/init")
    result = lambda_function.lambda_handler(event, None)
    assert "初期化しました" in result["body"]


def test_body_invalid_json_is_400(make_event):
    event = make_event("POST", "/numbers")
    event["body"] = "{not json"
    result = lambda_function.lambda_handler(event, None)
    assert result["statusCode"] == 400


def test_number_not_integer_is_400(call):
    call("POST", "/init")
    status, body = call("POST", "/number", {"number": "abc"})
    assert status == 400
    assert "message" in body


def test_numbers_how_many_not_integer_is_400(call):
    call("POST", "/init")
    status, body = call("POST", "/numbers", {"how_many": "abc"})
    assert status == 400
    assert "message" in body
