# bottle-rest-api

This is a REST API with [Bottle.py](https://bottlepy.org/docs/0.12/), [Peewee ORM](http://docs.peewee-orm.com/en/latest/), [Marshmallow](https://marshmallow.readthedocs.io/en/stable/) and [PyJWT](https://pyjwt.readthedocs.io/en/stable/).


## Overview: Bottle REST API

Problem Statement proposed by [AIMO](https://github.com/aimo)

Repo: https://github.com/aimo/technical-test-backend 

**See the details in** [ProblemStatement.md](ProblemStatement.md)


## Table of Contents

* [Overview](#bottle-rest-api)
* [Main Dependencies](#Main-Dependencies)
* [Python Configuration](#Python-Configuration)
* [Project Configuration](#Project-Configuration)


## Main Dependencies

    Python      ~3.8
    Bottle      ~0.12
    Peewee      ~3.14
    marshmallow ~3.12
    PyJWT       ~2.1

For more details, see the [pyproject.toml file](pyproject.toml).

## Python Configuration

- [Install Pyenv](https://github.com/pyenv/pyenv-installer)
- Install Python ~3.8:

    If you want to see **all available versions of Python**:

        $ pyenv install --list

    Now install the version you want of Python 3.8. e.g.:

        $ pyenv install 3.8.10

- [Install Poetry](https://python-poetry.org/docs/#installation)

- Configure the creation of the **virtual environment within the project:**

        $ vim $HOME/.bashrc

    **Add these lines to the end of the file:**

        # Poetry
        export POETRY_VIRTUALENVS_IN_PROJECT=1

## Project Configuration

- Clone this repo:

        $ git clone https://github.com/hugofer93/aimo-api.git

- Create `.env` file based on `.env.sample`:

        $ cp .env.sample .env

- **Activate the installed Python 3.8 version**. e.g.:

        $ pyenv shell 3.8.10

- Install dependencies **in Production environment:**

        $ poetry install --no-dev

    **For Development environment:**

        $ poetry install

- Activate virtual environment (optional):

        $ poetry shell

    Alternatively you can run without activating the virtual environment:

        $ poetry run <commands described below>

    e.g.:

        $ poetry run python file.py

- If you are in development environment:

        $ python server.py

    In another terminal:

        $ python client.py
