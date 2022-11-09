# DevOps Apprenticeship: Project Exercise

> If you are using GitPod for the project exercise (i.e. you cannot use your local machine) then you'll want to launch a VM using the [following link](https://gitpod.io/#https://github.com/CorndelWithSoftwire/DevOps-Course-Starter). Note this VM comes pre-setup with Python & Poetry pre-installed.

## System Requirements

The project uses poetry for Python to create an isolated environment and manage package dependencies. To prepare your system, ensure you have an official distribution of Python version 3.7+ and install Poetry using one of the following commands (as instructed by the [poetry documentation](https://python-poetry.org/docs/#system-requirements)):

### Poetry installation (Bash)

```bash
curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/install-poetry.py | python -
```

### Poetry installation (PowerShell)

```powershell
(Invoke-WebRequest -Uri https://raw.githubusercontent.com/python-poetry/poetry/master/install-poetry.py -UseBasicParsing).Content | python -
```

## Dependencies

The project uses a virtual environment to isolate package dependencies. To create the virtual environment and install required packages, run the following from your preferred shell:

```bash
$ poetry install
```

You'll also need to clone a new `.env` file from the `.env.template` to store local configuration options. This is a one-time operation on first setup:

```bash
$ cp .env.template .env  # (first time only)
```

The `.env` file is used by flask to set environment variables when running `flask run`. This enables things like development mode (which also enables features like hot reloading when you make a file change). There's also a [SECRET_KEY](https://flask.palletsprojects.com/en/1.1.x/config/#SECRET_KEY) variable which is used to encrypt the flask session cookie.

You will also need to [create a Trello account](https://trello.com/signup) (or login if you have one already) and generate an API key and token by following [these instructions](https://trello.com/app-key). The key and token should then be added to the relevant variables in your `.env` file.

This app will manage cards on a board of your choosing to keep track of 'to-do's. Either create a new board, or choose an existing one, and add its ID to the `BOARD_ID` variable in the `.env` file. This ID can be found in the URL in the browser when the board is open. Then add the names of the columns you wish to use for the "NOT_STARTED_LIST_NAME", "DOING_LIST_NAME" and "DONE_LIST_NAME" options to the `.env` file.  

## Tests

All tests are located in the `/tests` folder in the route directory.

Tests can be run by running:
```bash
$ poetry run pytest
```

## Running the App

Once the all dependencies have been installed, start the Flask app in development mode within the Poetry environment by running:
```bash
$ poetry run flask run
```

You should see output similar to the following:
```bash
 * Serving Flask app "app" (lazy loading)
 * Environment: development
 * Debug mode: on
 * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
 * Restarting with fsevents reloader
 * Debugger is active!
 * Debugger PIN: 226-556-590
```
Now visit [`http://localhost:5000/`](http://localhost:5000/) in your web browser to view the app.

## Using Ansible to Privision a VM from a Control Node

These instuctions assume that all target VMs used have the control node's public key listed in `~/.ssh/authorized_keys`, meaning no password is required for an ssh connection between the control node and managed VMs.  

It is also assumed that all VMs can be logged into with the same username. In this case, it is set to 'ec2-user', but can be consigured by editing the `remote_user` option at the top of file `ansible/ansible_playbook.yml`.  

The list of managed VMs can be configured from the `[managed_nodes]` section of `ansible/ansible_inventory`.  

To provision the VMs, run the following command from the route directory of this repo:
```bash
ansible-playbook ansible/ansible-playbook.yml -i ansible/ansible-inventory
```

The ToDo app should then be availble on each of the VMs at `http://host.ip.address:5000`.

## Using Docker  

This project includes a dockerfile allowing it to be run in a docker container for development or production purposes.

### Development

Build the docker container for development by running the folling command from the root of the project directory:
```bash
docker build --target development --tag todo-app:dev .
```

And run the container by running the following command from the root of the project directory, replacing `<port>` with the port that you want the site to be available on:
```bash
docker run --env-file .env -p <port>:5000 --mount type=bind,source="$(pwd)"/todo_app,target=/app/todo_app todo-app:dev
```

The site can then be accessed by navigating to `http://localhost:<port>` in a browser, replacing `<port>` with the value specified in the previous command.

In development mode, hot reloading is enabled and changes in the local file system should reflect in the site.

### Production

Build the docker container for development by running the folling command from the root of the project directory:
```bash
docker build --target production --tag todo-app:prod .
```

And run the container by running the following command from the root of the project directory, replacing `<port>` with the port that you want the site to be available on:
```bash
docker run --env-file .env -p <port>:8000 todo-app:prod
```

The site can then be accessed by navigating to `http://localhost:<port>` in a browser, replacing `<port>` with the value specified in the previous command.

Hot reloading is not enabled in production mode and to see any changes, the container will have to be rebuild and then rerun.
