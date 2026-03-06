import pytest
from sentiment_app import app

@pytest.fixture
def client():
    app.testing = True
    return app.test_client()

def test_positive(client):
    response = client.post("/analyze", json={"text": "happy"})
    assert response.status_code == 200

def test_missing_text(client):
    response = client.post("/analyze", json={})
    assert response.status_code == 400

def test_block_word(client):
    response = client.post("/block", json={"word": "bad"})
    assert response.status_code == 200