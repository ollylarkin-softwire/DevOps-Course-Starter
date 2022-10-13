import pytest
from dotenv import load_dotenv, find_dotenv
from todo_app import app
import requests
import os
from datetime import datetime, timedelta

NOW = datetime.now()

NOT_STARTED_LIST_ID = 'not-started-list-id'
DOING_LIST_ID = 'doing-list-id'
DONE_LIST_ID = 'done-list-id'

TEST_CARDS = [
    {
        'id': 'card-1-id',
        'name': 'test-card-1',
        'idList': NOT_STARTED_LIST_ID,
        'dateLastActivity': NOW.strftime('%Y-%m-%dT%H:%M:%S.%fZ'),
    },
    {
        'id': 'card-2-id',
        'name': 'test-card-2',
        'idList': NOT_STARTED_LIST_ID,
        'dateLastActivity': (NOW - timedelta(days=2)).strftime('%Y-%m-%dT%H:%M:%S.%fZ'),
    },
]

class StubResponse():
    def __init__(self, fake_response_data):
        self.fake_response_data = fake_response_data
    
    def json(self):
        return self.fake_response_data

    def raise_for_status(self):
        pass

def trello_request_stub(method, url, params):
    test_board_id = os.environ.get('BOARD_ID')
    fake_response_data = None
    if method == 'GET' and url == f'https://api.trello.com/1/boards/{test_board_id}/lists':
        fake_response_data = [
            {
                'id': NOT_STARTED_LIST_ID,
                'name': os.environ.get('NOT_STARTED_LIST_NAME'),
            },
            {
                'id': DOING_LIST_ID,
                'name': os.environ.get('DOING_LIST_NAME'),
            },
            {
                'id': DONE_LIST_ID,
                'name': os.environ.get('DONE_LIST_NAME'),
            },
        ]
    elif method == 'GET' and url == f'https://api.trello.com/1/boards/{test_board_id}/cards/open':
        fake_response_data = TEST_CARDS
    return StubResponse(fake_response_data)

@pytest.fixture
def client():
    file_path = find_dotenv('.env.test')
    load_dotenv(file_path, override=True)

    test_app = app.create_app()

    with test_app.test_client() as client:
        yield client

def test_index_page(monkeypatch, client):
    monkeypatch.setattr(requests, 'request', trello_request_stub)
    response = client.get('/')
    data = response.data.decode()
    assert response.status_code == 200
    for card in TEST_CARDS:
        if card['idList'] != DONE_LIST_ID or datetime.strptime(card['dateLastActivity'], '%Y-%m-%dT%H:%M:%S.%fZ').date() == NOW.date():
            assert card['name'] in data
        else:
            # should not be visible before "show more" button is clicked
            assert card['name'] not in data
