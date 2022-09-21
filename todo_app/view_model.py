from todo_app.data.status import NOT_STARTED_STATUS, DOING_STATUS, DONE_STATUS
from datetime import datetime

class ViewModel:
    def __init__(self, title_field_name, items, should_show_all_done_items = False):
        self._title_field_name = title_field_name
        self._items = items
        self._should_show_all_done_items = should_show_all_done_items

    @property
    def title_field_name(self):
        return self._title_field_name

    @property
    def should_show_all_done_items(self):
        return self._should_show_all_done_items

    @property
    def not_started_items(self):
        return list(filter(lambda t: t.status == NOT_STARTED_STATUS, self._items))

    @property
    def doing_items(self):
        return list(filter(lambda t: t.status == DOING_STATUS, self._items))

    @property
    def done_items(self):
        return list(filter(lambda t: t.status == DONE_STATUS, self._items))

    @property
    def recent_done_items(self):
        return list(filter(lambda t: t.status == DONE_STATUS and t.last_edit.date() == datetime.now().date(), self._items))

    @property
    def older_done_items(self):
        return list(filter(lambda t: t.status == DONE_STATUS and t.last_edit.date() < datetime.now().date(), self._items))

    @property
    def there_are_older_items(self):
        return len(self.older_done_items) > 0
