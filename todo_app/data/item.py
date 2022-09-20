from todo_app.data.status import NOT_STARTED_STATUS, DOING_STATUS, DONE_STATUS

class Item:
    def __init__(self, id, name, status = NOT_STARTED_STATUS):
        self.id = id
        self.name = name
        self.status = status

    @classmethod
    def from_trello(cls, trello, card):
        if card['idList'] == trello.list_ids.not_started:
            status = NOT_STARTED_STATUS
        elif card['idList'] == trello.list_ids.doing:
            status = DOING_STATUS
        elif card['idList'] == trello.list_ids.done:
            status = DONE_STATUS
        else:
            raise Exception('Invalid list name')
        
        return cls(card['id'], card['name'], status)
