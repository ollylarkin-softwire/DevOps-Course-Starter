from todo_app.data.status import NOT_STARTED_STATUS, DOING_STATUS, DONE_STATUS

class ViewModel:
    def __init__(self, title_field_name, items):
        self._title_field_name = title_field_name
        self._items = items

    @property
    def title_field_name(self):
        return self._title_field_name

    @property
    def items(self):
        return self._items

    @property
    def not_started_todos(self):
        return list(filter(lambda t: t.status == NOT_STARTED_STATUS, self._items))

    @property
    def doing_todos(self):
        return list(filter(lambda t: t.status == DOING_STATUS, self._items))

    @property
    def done_todos(self):
        return list(filter(lambda t: t.status == DONE_STATUS, self._items))
