FROM python:3.10-buster as base
RUN curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/install-poetry.py | python -
ENV PATH=$PATH:/root/.local/share/pypoetry/venv/bin/
COPY poetry.toml pyproject.toml /app/
WORKDIR /app
RUN poetry install

FROM base as production
EXPOSE 8000
COPY todo_app /app/todo_app
ENTRYPOINT poetry run gunicorn --bind 0.0.0.0 "todo_app.app:create_app()"

FROM base as development
EXPOSE 5000
ENTRYPOINT poetry run flask run --host 0.0.0.0

FROM base as test
COPY todo_app /app/todo_app
COPY tests /app/tests
COPY .env.test /app/.env.test
ENTRYPOINT ["poetry", "run", "pytest"]
