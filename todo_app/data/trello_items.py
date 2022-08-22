from todo_app.data.trello_api_utils import trello_request, BOARD_ID, NOT_STARTED_LIST_ID, DONE_LIST_ID
from todo_app.data.item import Item
import requests


def get_items():
    """
    Fetches all open cards from Trello board

    Returns:
        list: The list of open cards
    """
    r = trello_request('GET', f'/boards/{BOARD_ID}/cards/open')
    r.raise_for_status()
    cards = r.json()
    return [Item.from_trello(card) for card in cards]


def get_item(id):
    """
    Fetches the saved card with the specified ID

    Args:
        id: The ID of the card

    Returns:
        item: The saved item, or None if no items match the specified ID.
    """
    r = trello_request('GET', f'/cards/{id}')
    if r.status_code == requests.codes.not_found:
        return None
    r.raise_for_status()
    card = r.json()
    return Item.from_trello(card)


def add_item(title):
    r = trello_request('POST', '/cards', {
        'name': title,
        'idList': NOT_STARTED_LIST_ID,
    })
    r.raise_for_status()
    added_card = r.json()
    return Item.from_trello(added_card)


def complete_item(id):
    r = trello_request('PUT', f'/cards/{id}', {
        'idList': DONE_LIST_ID,
    })
    r.raise_for_status()
    updated_card = r.json()
    return Item.from_trello(updated_card)


def reset_item(id):
    r = trello_request('PUT', f'/cards/{id}', {
        'idList': NOT_STARTED_LIST_ID,
    })
    r.raise_for_status()
    updated_card = r.json()
    return Item.from_trello(updated_card)
