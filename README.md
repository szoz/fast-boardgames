# fast-boardgames

Backend web application with REST API created using [FastAPI](https://fastapi.tiangolo.com/). Application contains data
about top 100 boardgames from BoardGameGeek stored in PostgreSQL database. Application in available on Heroku:
`https://fast-boardgames.herokuapp.com/`

## Technologies

Project is created with:

* Python 3.8
* [Pipenv](https://github.com/pypa/pipenv)
* [FastAPI](https://fastapi.tiangolo.com/)

[Pytest](https://docs.pytest.org/en/6.2.x/) is used for testing.

## Setup

To run this project install dependencies using Pipenv for production environment:

```
$ pipenv install --ignore-pipfile
```

or development environment:

```
$ pipenv install --dev
```

Project requires PostgreSQL database with certain schema. In order to create required database use dump
from `/database_restore` folder.

Add 2 environment variables:
* `DATABASE_URL` - URL to database with login and password.
* `SECRET_KEY` - random string for password hashing (recommended 24-bit hex value).

Finally, run application with Uvicorn:

```
$ uvicorn main:app
```