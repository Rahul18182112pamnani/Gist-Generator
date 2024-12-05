import pytest
from app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_home_page(client):
    response = client.get("/")
    assert response.status_code == 200
    assert b"GitHub Gist Viewer" in response.data

def test_get_gists_success(client, mocker):
    mock_response = [
        {
            "created_at": "2024-11-01T12:00:00Z",
            "description": "Test Gist 1",
            "html_url": "https://gist.github.com/1"
        }
    ]
    mocker.patch('app.fetch_gists', return_value=mock_response)
    response = client.post("/get_gists", data={"username": "testuser"})
    assert response.status_code == 200
    data = response.json
    assert "November 2024" in data

def test_get_gists_user_not_found(client, mocker):
    mocker.patch('app.fetch_gists', return_value=None)
    response = client.post("/get_gists", data={"username": "nonexistentuser"})
    assert response.status_code == 404
    assert b"User not found" in response.data
