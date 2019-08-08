[![CircleCI](https://circleci.com/gh/junioweb/work-at-olist.svg?style=svg)](https://circleci.com/gh/junioweb/work-at-olist)

# Interview - Call Details

The test specification is described [here](SPECIFICATION.md). The application is
hosted on Heroku with the Base URL: `workatolist-calls.herokuapp.com/api/v1` and
the API documentation can be checked [here](https://workatolist-calls.herokuapp.com/docs/).

## Description

This application provide a HTTP REST API, receiving call detail records and
calculating monthly accounts for a particular phone number.

## Usage

To run this app you'll need:

* Python 3.7+ (It should work with older Python 3 version).
* PIP

There is two easy ways to run and test this app.

### Locally

1. Clone this repository.
2. Install requirements: `pip install -r requirements-local.txt`
3. Create a `.env` file. Use `local.env` as a example.
4. Run: `python manage.py runserver`

### Heroku

1. Clone this repository.
2. Install [`heroku-cli`](https://devcenter.heroku.com/articles/heroku-cli).
3. Create the heroku app and deploy it.

Or go through the link: `https://workatolist-calls.herokuapp.com/docs/`

## Testing

To test, just run `python manage.py test`.

## Implementation Details

About the development environment, I'm developing this project using a Notebook,
running openSUSE Tumbleweed. I have written this text and code entirely in PyCharm.

To develop this app I added some extra dependencies:

* *[Django](https://github.com/django/django):* Django is a high-level Python Web framework that encourages rapid development and clean, pragmatic design
* *[djangorestframework](https://github.com/encode/django-rest-framework):* Django REST framework is a powerful and flexible toolkit for building Web APIs.
* *[prettyconf](https://github.com/osantana/prettyconf):* Pretty Conf is a Python library created to make easy the separation of configuration and code following the recomendations of 12 Factor's topic about configs.
* *[dj-database-url](https://github.com/kennethreitz/dj-database-url):* This simple Django utility allows you to utilize the 12factor inspired DATABASE_URL environment variable to configure your Django application.
* *[drf-yasg](https://github.com/axnsan12/drf-yasg):* Automated generation of real Swagger/OpenAPI 2.0 schemas from Django REST Framework code.
* *[Markdown](https://pypi.org/project/Markdown/):* Markdown support for the browsable API.
* *[django-filter](https://github.com/carltongibson/django-filter):* A generic system for filtering Django QuerySets based on user selections.
* *[packaging](https://github.com/pypa/packaging):* Core utilities for Python packages.
* *[flake8](https://gitlab.com/pycqa/flake8):* Python tool that glues together pep8, pyflakes, mccabe, and third-party plugins to check the style and quality of some python code.
* *[coverage](https://github.com/nedbat/coveragepy):* Code coverage measurement for Python.
* *[django-heroku](https://github.com/heroku/django-heroku):* A Django library for Heroku apps.
* *[gunicorn](https://github.com/benoitc/gunicorn):* WSGI HTTP Server for UNIX, fast clients and sleepy applications.
* *[psycopg2](https://github.com/psycopg/psycopg2):* PostgreSQL database adapter for the Python programming language.
