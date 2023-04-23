#!/bin/sh

systemctl is-active --quiet postgresql.service || systemctl start postgresql.service
. venv/bin/activate
export FLASK_APP=app_factory
export FLASK_DEBUG=1
flask run
