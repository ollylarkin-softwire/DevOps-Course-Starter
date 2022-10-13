import pytest
from todo_app.view_model import ViewModel
from todo_app.data.item import Item
from todo_app.data.status import NOT_STARTED_STATUS, DOING_STATUS, DONE_STATUS
from datetime import datetime, timedelta

now = datetime.now()

test_items = [
    Item('id1', 'item1', NOT_STARTED_STATUS),
    Item('id2', 'item2', NOT_STARTED_STATUS),
    Item('id3', 'item3', NOT_STARTED_STATUS),
    Item('id4', 'item4', DOING_STATUS),
    Item('id5', 'item5', DOING_STATUS),
    Item('id6', 'item6', DONE_STATUS, datetime(now.year, now.month, now.day, 0, 0, 0)),
    Item('id7', 'item7', DONE_STATUS, datetime(now.year, now.month, now.day, 12, 0, 0)),
    Item('id8', 'item8', DONE_STATUS, datetime(now.year, now.month, now.day, 0, 0, 0) - timedelta(seconds=1)),
]

def test_not_started_items():
    view_model = ViewModel('title_field', test_items)
    not_started_items = view_model.not_started_items
    assert len(not_started_items) == 3
    for not_started_item in not_started_items:
        assert not_started_item.status == NOT_STARTED_STATUS

def test_doing_items():
    view_model = ViewModel('title_field', test_items)
    doing_items = view_model.doing_items
    assert len(doing_items) == 2
    for doing_item in doing_items:
        assert doing_item.status == DOING_STATUS

def test_done_items():
    view_model = ViewModel('title_field', test_items)
    done_items = view_model.done_items
    assert len(done_items) == 3
    for done_item in done_items:
        assert done_item.status == DONE_STATUS

def test_recent_done_items():
    view_model = ViewModel('title_field', test_items)
    recent_done_items = view_model.recent_done_items
    assert len(recent_done_items) == 2
    for recent_done_item in recent_done_items:
        assert recent_done_item.status == DONE_STATUS
        assert recent_done_item.last_edit.date() == now.date()

def test_older_done_items():
    view_model = ViewModel('title_field', test_items)
    older_done_items = view_model.older_done_items
    assert len(older_done_items) == 1
    for older_done_item in older_done_items:
        assert older_done_item.status == DONE_STATUS
        assert older_done_item.last_edit.date() < now.date()
