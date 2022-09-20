from flask import Flask, render_template, request, redirect, url_for
from todo_app.data.trello_items import get_items, add_item, complete_item, reset_item
from todo_app.data.status import NOT_STARTED_STATUS, DONE_STATUS

from todo_app.flask_config import Config

app = Flask(__name__)
app.config.from_object(Config())

TITLE_FIELD_NAME = 'title' 

@app.route('/')
def index():
    todos = get_items()
    return render_template(
        'index.html',
        title_field_name=TITLE_FIELD_NAME,
        not_started_todos=filter(lambda t: t.status == NOT_STARTED_STATUS, todos),
        done_todos=filter(lambda t: t.status == DONE_STATUS, todos),
    )

@app.route('/new-todo', methods=['POST'])
def new_todo():
    title = request.form.get(TITLE_FIELD_NAME)
    add_item(title)
    return redirect(url_for('index'))

@app.route('/complete-todo/<id>', methods=['GET'])
def complete_todo(id):
    complete_item(id)
    return redirect(url_for('index'))

@app.route('/reset-todo/<id>', methods=['GET'])
def reset_todo(id):
    reset_item(id)
    return redirect(url_for('index'))
