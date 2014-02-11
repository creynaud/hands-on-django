Notes Django app
================

This is a Django application example for the "Hands on Django" JDuchess Swiss workshop:
http://www.eventbrite.fr/e/billets-hands-on-django-et-deploiement-sur-le-cloud-avec-heroku-10260767231

You can have a look at the running app here: https://django-notes.herokuapp.com/ (runs on Heroku Europe).

Installation
------------

Requirements:

* Python 2.7.4 + dev (ubuntu package: python-dev)
* PostgreSQL (ubuntu packages: postgresql postgresql-server-dev-?.?, mac os: http://postgresapp.com/)
* ubuntu package: daemontools (for "envdir")
* ubuntu package: pyflakes (for "flake8")
* ubuntu package: virtualenvwrapper (for "mkvirtualenv") (reopen a new shell after install)

Getting the code::

    git clone https://github.com/creynaud/jduchess-ch-hands-on-django
    cd jduchess-ch-hands-on-django
    mkvirtualenv -p python2.7 notes
    add2virtualenv .
    pip install -r requirements-dev.txt

Configuration
-------------

The notes server relies on environment variables for its configuration. The required environment variables are:

* ``DJANGO_SETTINGS_MODULE``: set it to ``notes.settings``.
* ``SECRET_KEY``: set to a long random string.
* ``ALLOWED_HOSTS``: space-separated list of hosts which serve the web app.
  E.g. ``www.awesomenotes.net awesomenotes.net``.
* ``FROM_EMAIL``: the email address that sends automated emails (password
  lost, etc.). E.g. ``Notes <info@awesomenotes.net>``.
* ``DATABASE_URL``: a heroku-like database URL. E.g.
  ``postgres://user:password@host:port/database``. For development, modify the DATABASE_URL in the env director with your project's path if you want to use sqlite.
  Otherwise put the URL of your postgresql database.
* ``SMTP_URL``: your smtp URL, e.g. //username:password@host:port?sender=info@awesomenotes.net

Optionally you can customize:

* ``DEBUG``: set it to a non-empty value to enable the Django debug mode.

"Sync" the db (django)::

    envdir env python manage.py syncdb
    # enter an email for your *admin* user and a password

Then you can run and create stuff manually to see the thing::

    envdir env python manage.py runserver
    http://127.0.0.1:8000/admin
    http://127.0.0.1:8000

Development
-----------

Listing available commands::

    envdir env python manage.py

Before commiting anything, make sure to:

Run the tests::

    envdir env python manage.py test

Run the source code checker::

    flake8

The Django debug toolbar is enabled when the ``DEBUG`` environment variable is
true.

Environment variables for development are set in the ``env`` directory.
