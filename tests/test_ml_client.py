import os
import pytest
from mongomock import MongoClient
from unittest.mock import patch, MagicMock
from machineLearningClient.app import create_app, predict


def test_sanity_check():
    expected = True  # the value we expect to be present
    actual = True  # the value we see in reality
    assert actual == expected, "Expected True to be equal to True!"

def test_predict():
    with patch('openai.chat.completions.create') as mock_create:
        mock_completion = MagicMock()
        mock_create.return_value = mock_completion
        location = "New York New York United States of America"
        predict(location, "mock key")
        mock_create.assert_called_once_with(
            messages=[{"role": "system", "content": "You are an intelligent assistant."},
                {"role": "user", "content": "List the 5 best things to do in " + location}],
            model="gpt-3.5-turbo"
        )

@pytest.fixture
def db():
    client = MongoClient()
    db = client.db.collection
    yield db
    client.drop_database(db)


def test_ML_client(db, monkeypatch):
    user_data = {
        "name": "Test User",
        "latitude": 40,
        "longitude": -74,
        "city": "New York",
        "region": "New York",
        "country": "United States of America",
        "ml_response": "",
    }
    db.insert_one(user_data)
    def mock_predict(user_loc, openai_key):
        return "Mock ML Response"
    monkeypatch.setattr("machineLearningClient.app.predict", mock_predict)
    app = create_app(db, "mock key")
    app.config["TESTING"] = True
    client = app.test_client()
    response = client.get("/ml_result")
    assert response.status_code == 200


def test_ML_client_fail(db, monkeypatch):
    user_data = {
        "name": "Test",
        "latitude": 40,
        "longitude": -74,
        "city": "New York",
        "region": "New York",
        "country": "United States of America",
        "ml_response": "",
    }
    db.insert_one(user_data)
    def mock_predict(user_loc, openai_key):
        return "Mock ML Response"
    monkeypatch.setattr("machineLearningClient.app.predict", mock_predict)
    app = create_app(db, "mock key")
    app.config["TESTING"] = True
    client = app.test_client()
    response = client.get("/ml_result")
    assert response.status_code == 404
