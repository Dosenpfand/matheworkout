# MatheWorkout

[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

Practice for the Austrian high school certificate exam (matura) in maths.

## Run

```
export FLASK_APP=app/__init__.py
export FLASK_DEBUG=1
flask fab create-admin
flask run
```

## Setup local development
Install additional dependencies
```
pip install -r requirements-dev.txt
```
and install the pre-commit hooks
```
pre-commit install
```

## Migrate database schema
```
flask db migrate -m "message."
flask db upgrade
```

## Redeploy from backup

Create database and user:
```bash
sudo -u postgres psql
# create database matheueben;
# create user mathesuper with encrypted password '123456';
# grant all privileges on database matheueben to mathesuper;
```

Import database backup:
```bash
sudo -u postgres psql matheueben < backup.sql
```

Clean up database:
```bash
flask fab security-cleanup
flask fab create-db
```

## Live instance

A live instance of the project is reachable at [matheworkout.at](https://matheworkout.at/).
