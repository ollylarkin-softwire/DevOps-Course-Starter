import pytest
from todo_app.view_model import ViewModel
from todo_app.data.item import Item
from todo_app.data.status import NOT_STARTED_STATUS, DOING_STATUS, DONE_STATUS

test_items = [
    Item('id1', 'item1', NOT_STARTED_STATUS),
    Item('id2', 'item2', NOT_STARTED_STATUS),
    Item('id3', 'item3', NOT_STARTED_STATUS),
    Item('id4', 'item4', DOING_STATUS),
    Item('id5', 'item5', DOING_STATUS),
    Item('id6', 'item6', DONE_STATUS),
]

def test_not_started_todos():
    view_model = ViewModel('title_field', test_items)
    not_started_todos = view_model.not_started_todos
    assert len(not_started_todos) == 3
    for not_started_todo in not_started_todos:
        assert next(todo for todo in test_items if todo.id == not_started_todo.id).status == NOT_STARTED_STATUS

def test_doing_todos():
    view_model = ViewModel('title_field', test_items)
    doing_todos = view_model.doing_todos
    assert len(doing_todos) == 2
    for doing_todo in doing_todos:
        assert next(todo for todo in test_items if todo.id == doing_todo.id).status == DOING_STATUS

def test_done_todos():
    view_model = ViewModel('title_field', test_items)
    done_todos = view_model.done_todos
    assert len(done_todos) == 1
    for done_todo in done_todos:
        assert next(todo for todo in test_items if todo.id == done_todo.id).status == DONE_STATUS
