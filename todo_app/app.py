from flask import Flask, render_template, request, redirect, url_for
from todo_app.data.trello_items import TrelloItems
from todo_app.view_model import ViewModel

from todo_app.flask_config import Config

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config())
    trello_items = TrelloItems()

    TITLE_FIELD_NAME = 'title'

    @app.route('/')
    def index():
        todos = trello_items.get_items()
        should_show_all_done_items = request.args.get('should_show_all_done_items', default=False, type=bool)
        return render_template('index.html', view_model=ViewModel(
            title_field_name=TITLE_FIELD_NAME,
            items=todos,
            should_show_all_done_items=should_show_all_done_items,
        ))

    @app.route('/new-todo', methods=['POST'])
    def new_todo():
        title = request.form.get(TITLE_FIELD_NAME)
        trello_items.add_item(title)
        return redirect(url_for('index'))

    @app.route('/start-todo/<id>', methods=['GET'])
    def start_todo(id):
        trello_items.start_item(id)
        return redirect(url_for('index'))

    @app.route('/complete-todo/<id>', methods=['GET'])
    def complete_todo(id):
        trello_items.complete_item(id)
        return redirect(url_for('index'))

    @app.route('/reset-todo/<id>', methods=['GET'])
    def reset_todo(id):
        trello_items.reset_item(id)
        return redirect(url_for('index'))

    return app
