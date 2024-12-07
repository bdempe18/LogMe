# LogMe

LogMe is a log management tool designed to be run locally and aid in presentation, analysis, and
management of server logs. It currently supports Laravel logs with the intention to quickly add
support for Django logs.

## Dependencies
You need a current version of Python (3.11 or newer) as well as a
[Poetry](https://python-poetry.org/). If you don't have Poetry, I recommend using Pipx to install
it.

## Installation

#### Project Dependencies
After cloning the repository, navigate to the project root and install the additional dependencies.
Poetry will install and resolve all project dependencies.

```console
poetry install
```

#### Database
LogMe uses a postgres database to locally store logs. There are many ways to configure the local
database, but the following assumes that you have Postgres running globally.

```console
sudo -u postgres psql

CREATE DATABASE logme;
CREATE USER djangouser with PASSWORD 'django';
GRANT ALL PRIVILEGES ON DATABASE logme to djangouser;
ALTER ROLE djangouser SET client_encoding to 'utf8';
ALTER ROLE djangouser SET default_transaction_isolation to 'read committed';
ALTER ROLE djangouser SET timezone TO 'UTC';
\q
echo "DATABASE_URL=postgres://djangouser/django@127.0.0.1/logme" >> .env
```

You can (and should) alter the username and password to fit your local configuration.

### Asserts
Navigation to the project static directory and build.

```console
cd logme/static
npm install
npm run build
```

### Launch the Localserver
Navigate back to the project root, drop into the poetry shell, and you are good to go!

```console
poetry shell
./manage.py runserver_plus
```
