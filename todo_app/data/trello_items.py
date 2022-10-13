from todo_app.data.trello_api_utils import Trello
from todo_app.data.item import Item
import requests

class TrelloItems:
    def __init__(self):
        self.trello = Trello()

    def get_items(self):
        """
        Fetches all open cards from Trello board

        Returns:
            list: The list of open cards
        """
        r = self.trello.request(f'/boards/{self.trello.board_id}/cards/open')
        r.raise_for_status()
        cards = r.json()
        return [Item.from_trello(self.trello, card) for card in cards]


    def get_item(self, id):
        """
        Fetches the saved card with the specified ID

        Args:
            id: The ID of the card

        Returns:
            item: The saved item, or None if no items match the specified ID.
        """
        r = self.trello.request(f'/cards/{id}')
        if r.status_code == requests.codes.not_found:
            return None
        r.raise_for_status()
        card = r.json()
        return Item.from_trello(self.trello, card)


    def add_item(self, title):
        r = self.trello.request('/cards', 'POST', {
            'name': title,
            'idList': self.trello.list_ids.not_started,
        })
        r.raise_for_status()
        added_card = r.json()
        return Item.from_trello(self.trello, added_card)


    def start_item(self, id):
        r = self.trello.request(f'/cards/{id}', 'PUT', {
            'idList': self.trello.list_ids.doing,
        })
        r.raise_for_status()
        updated_card = r.json()
        return Item.from_trello(self.trello, updated_card)


    def complete_item(self, id):
        r = self.trello.request(f'/cards/{id}', 'PUT', {
            'idList': self.trello.list_ids.done,
        })
        r.raise_for_status()
        updated_card = r.json()
        return Item.from_trello(self.trello, updated_card)


    def reset_item(self, id):
        r = self.trello.request(f'/cards/{id}', 'PUT', {
            'idList': self.trello.list_ids.not_started,
        })
        r.raise_for_status()
        updated_card = r.json()
        return Item.from_trello(self.trello, updated_card)
