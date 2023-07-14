#!/bin/sh

pybabel compile -d app/translations
flask db upgrade || flask fab create-db
