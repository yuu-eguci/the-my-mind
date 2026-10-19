import pytest

from local_test import app


@pytest.fixture
def client():
    return app.test_client()


def test_health(client):
    response = client.get("/")
    assert response.status_code == 200
    assert response.get_json() == {"statusCode": 200, "body": {"message": "OK"}}


def test_not_found(client):
    response = client.get("/unknown")
    assert response.status_code == 404
    assert response.get_json()["statusCode"] == 404


def test_game_round_trip(client):
    assert client.post("/init").get_json()["statusCode"] == 200
    response = client.post("/numbers", json={"how_many": 2})
    assert response.status_code == 200
    numbers = sorted(response.get_json()["body"]["numbers"])
    response = client.post("/number", json={"number": numbers[0]})
    assert response.get_json()["body"]["numbers_out"] == [numbers[0]]
    response = client.post("/number", json={"number": numbers[0]})
    assert response.status_code == 409
    assert response.get_json() == {
        "statusCode": 409,
        "body": response.get_json()["body"],
    }


def test_cors_header(client):
    response = client.get("/", headers={"Origin": "http://localhost:8080"})
    assert "Access-Control-Allow-Origin" in response.headers
