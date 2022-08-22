from todo_app.data.status import NOT_STARTED_STATUS, DONE_STATUS
from todo_app.data.trello_api_utils import NOT_STARTED_LIST_ID, DONE_LIST_ID

class Item:
    def __init__(self, id, name, status = NOT_STARTED_STATUS):
        self.id = id
        self.name = name
        self.status = status

    @classmethod
    def from_trello(cls, card):
        if card['idList'] == NOT_STARTED_LIST_ID:
            status = NOT_STARTED_STATUS
        elif card['idList'] == DONE_LIST_ID:
            status = DONE_STATUS
        else:
            raise Exception('Invalid list name')
        
        return cls(card['id'], card['name'], status)
