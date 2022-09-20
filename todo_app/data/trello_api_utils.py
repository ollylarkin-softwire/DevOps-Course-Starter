import os
import requests

NOT_STARTED_LIST_NAME = 'To Do'
DONE_LIST_NAME = 'Done'

BOARD_ID = os.getenv('BOARD_ID')

def trello_request(method, url, params={}):
    BASE_URL = 'https://api.trello.com/1'
    API_KEY = os.getenv('TRELLO_API_KEY')
    API_TOKEN = os.getenv('TRELLO_API_TOKEN')
    BASE_QUERY_PARAMS = {
        'key': API_KEY,
        'token': API_TOKEN,
    }

    full_url = BASE_URL + url
    query_params = dict(BASE_QUERY_PARAMS, **params)
    return requests.request(method, full_url, params=query_params)

def get_lists():
    r = trello_request('GET', f'/boards/{BOARD_ID}/lists')
    r.raise_for_status()
    return r.json()

LISTS = get_lists()

NOT_STARTED_LIST_ID = next(list['id'] for list in LISTS if list['name'] == NOT_STARTED_LIST_NAME)
DONE_LIST_ID = next(list['id'] for list in LISTS if list['name'] == DONE_LIST_NAME)
