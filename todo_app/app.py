from flask import Flask, render_template, request, redirect, url_for
from todo_app.data.trello_items import get_items, add_item, start_item, complete_item, reset_item
from todo_app.view_model import ViewModel

from todo_app.flask_config import Config

app = Flask(__name__)
app.config.from_object(Config())

TITLE_FIELD_NAME = 'title'

@app.route('/')
def index():
    todos = get_items()
    return render_template('index.html', view_model=ViewModel(
        title_field_name=TITLE_FIELD_NAME,
        items=todos,
    ))

@app.route('/new-todo', methods=['POST'])
def new_todo():
    title = request.form.get(TITLE_FIELD_NAME)
    add_item(title)
    return redirect(url_for('index'))

@app.route('/start-todo/<id>', methods=['GET'])
def start_todo(id):
    start_item(id)
    return redirect(url_for('index'))

@app.route('/complete-todo/<id>', methods=['GET'])
def complete_todo(id):
    complete_item(id)
    return redirect(url_for('index'))

@app.route('/reset-todo/<id>', methods=['GET'])
def reset_todo(id):
    reset_item(id)
    return redirect(url_for('index'))
