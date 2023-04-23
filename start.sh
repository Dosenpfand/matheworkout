#! /usr/bin/env sh
set -e

service postgresql start

exec gunicorn --workers 5 --bind 0.0.0.0:8080 main:app
