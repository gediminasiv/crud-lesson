import pytest
import os
from main import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    os.environ['TESTING'] = "1"
    client = app.test_client()

    yield client

def cleanup():
    db = TinyDB('test_db.json')

    db.purge_tables()

def test_index_not_logged_in(client):
    response = client.get('/')

    assert b'Enter your name' in response.data

def test_index_logged_in(client):
    client = login(client)

    response = client.get('/')

    assert b'Enter your guess' in response.data

def test_index_log_out(client):
    client = login(client)

    response = client.get('/logout', follow_redirects=True)

    assert b'Enter your name' in response.data

def login(client):
    client.post('/login', data={
        "user-name": "Testas",
        "user-password": "Test1234",
        "user-email": "test@mail.comm"
    }, follow_redirects=True)

    return client
