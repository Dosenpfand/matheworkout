# Mathe-Matura-Quiz

## Run

```
export FLASK_APP=app/__init__.py
export FLASK_ENV=development
flask fab create-admin
flask run
```

## Migrate database schema
```
flask db migrate -m "message."
flask db upgrade
```

## TODO