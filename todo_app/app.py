from flask import Flask, render_template, request, redirect, url_for
from todo_app.data.session_items import get_items, add_item

from todo_app.flask_config import Config

app = Flask(__name__)
app.config.from_object(Config())


titleFieldName = 'title' 

@app.route('/')
def index():
    todos = get_items()
    return render_template('index.html', todos=todos, titleFieldName=titleFieldName)

@app.route('/new-todo', methods=["POST"])
def newTodo():
    title = request.form.get(titleFieldName)
    if title != '':
        add_item(title)
    return redirect(url_for('index'))
