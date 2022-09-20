from todo_app.data.trello_api_utils import Trello
from todo_app.data.item import Item
import requests

trello = Trello()

def get_items():
    """
    Fetches all open cards from Trello board

    Returns:
        list: The list of open cards
    """
    r = trello.request(f'/boards/{trello.board_id}/cards/open')
    r.raise_for_status()
    cards = r.json()
    return [Item.from_trello(trello, card) for card in cards]


def get_item(id):
    """
    Fetches the saved card with the specified ID

    Args:
        id: The ID of the card

    Returns:
        item: The saved item, or None if no items match the specified ID.
    """
    r = trello.request(f'/cards/{id}')
    if r.status_code == requests.codes.not_found:
        return None
    r.raise_for_status()
    card = r.json()
    return Item.from_trello(trello, card)


def add_item(title):
    r = trello.request('/cards', 'POST', {
        'name': title,
        'idList': trello.list_ids.not_started,
    })
    r.raise_for_status()
    added_card = r.json()
    return Item.from_trello(trello, added_card)


def start_item(id):
    r = trello.request(f'/cards/{id}', 'PUT', {
        'idList': trello.list_ids.doing,
    })
    r.raise_for_status()
    updated_card = r.json()
    return Item.from_trello(trello, updated_card)


def complete_item(id):
    r = trello.request(f'/cards/{id}', 'PUT', {
        'idList': trello.list_ids.done,
    })
    r.raise_for_status()
    updated_card = r.json()
    return Item.from_trello(trello, updated_card)


def reset_item(id):
    r = trello.request(f'/cards/{id}', 'PUT', {
        'idList': trello.list_ids.not_started,
    })
    r.raise_for_status()
    updated_card = r.json()
    return Item.from_trello(trello, updated_card)
