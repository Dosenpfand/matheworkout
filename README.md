# MatheWorkout

Practice for the Austrian high school certificate exam (matura) in maths.

## Run

```
export FLASK_APP=app/__init__.py
export FLASK_DEBUG=1
flask fab create-admin
flask run
```

## Setup local development
Dependencies are managed with [uv](https://docs.astral.sh/uv/) (`pyproject.toml` and `uv.lock`).
Install all dependencies including the development ones
```
uv sync
```
(add new ones with `uv add <package>`, update the lock file with `uv lock --upgrade`) and install the pre-commit hooks
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
# alter database matheueben owner to mathesuper;
```

Import database backup:
```bash
sudo -u postgres psql matheueben < backup.sql
```

or in the container:
```bash
psql -U db_user -h postgres -p 5432 -d db_database < backup.sql
```

Clean up database:
```bash
flask fab security-cleanup
flask fab create-db
```

## Live instance

A live instance of the project is reachable at [matheworkout.at](https://matheworkout.at/).
