import os
import requests

class ListNames:
    def __init__(self, not_started, doing, done):
        if not_started == None or doing == None or done == None:
            raise Exception('Could not get all list names from environment variables')
        self.not_started = not_started
        self.doing = doing
        self.done = done

class Ids:
    def __init__(self, not_started, doing, done):
        if not_started == None or doing == None or done == None:
            raise Exception('Couldn\'t find all required lists')
        self.not_started = not_started
        self.doing = doing
        self.done = done

class Trello:
    def __init__(self):
        self._lists = None
        self._ids = None
        self.board_id = os.getenv('BOARD_ID')
        self.list_names = ListNames(
            os.getenv('NOT_STARTED_LIST_NAME'),
            os.getenv('DOING_LIST_NAME'),
            os.getenv('DONE_LIST_NAME'),
        )

    def request(self, url, method='GET', params={}):
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

    @property
    def lists(self):
        if self._lists == None:
            r = self.request(f'/boards/{self.board_id}/lists')
            r.raise_for_status()
            self._lists = r.json()
        return self._lists

    @property
    def list_ids(self):
        if self._ids == None:
            self._ids = Ids(
                next(list['id'] for list in self.lists if list['name'] == self.list_names.not_started),
                next(list['id'] for list in self.lists if list['name'] == self.list_names.doing),
                next(list['id'] for list in self.lists if list['name'] == self.list_names.done),
            )
        return self._ids
