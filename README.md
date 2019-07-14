[![CircleCI](https://circleci.com/gh/junioweb/work-at-olist.svg?style=svg)](https://circleci.com/gh/junioweb/work-at-olist)

# Interview - Call Details

The test specification is described [here](SPECIFICATION.md). The application is
hosted on Heroku with the URL: `http://workatolist-calls.herokuapp.com` and
the API documentation can be checked [here](http://workatolist-calls.herokuapp.com/calls/docs/).

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

Or go through the link: `http://workatolist-calls.herokuapp.com`

## Testing

To test, just run `python manage.py test`.

## Implementation Details

About the development environment, I'm developing this project using a Notebook,
running openSUSE Tumbleweed. I have written this text and code entirely in PyCharm.

To develop this app I added some extra dependencies:

* *[Django](https://github.com/django/django):* Django is a high-level Python Web framework that encourages rapid development and clean, pragmatic design
* *[djangorestframework](https://github.com/encode/django-rest-framework/tree/master):* Django REST framework is a powerful and flexible toolkit for building Web APIs.
* *[prettyconf](https://github.com/osantana/prettyconf):* Pretty Conf is a Python library created to make easy the separation of configuration and code following the recomendations of 12 Factor's topic about configs.
* *[dj-database-url](https://github.com/kennethreitz/dj-database-url):* This simple Django utility allows you to utilize the 12factor inspired DATABASE_URL environment variable to configure your Django application.
* *[coreapi](https://github.com/core-api/python-client):* Schema generation support.
* *[Markdown](https://pypi.org/project/Markdown/):* Markdown support for the browsable API.
* *[django-filter](https://github.com/carltongibson/django-filter/tree/master):* Filtering support.
