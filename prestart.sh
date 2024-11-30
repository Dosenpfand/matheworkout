#!/bin/sh

if flask db current | grep "(head)"; then
    echo "Running database upgrade."
    flask db upgrade
else
    echo "Initizalizing database."
    flask fab create-db
    flask db stamp
    # TODO: Fix! user creation functionality broken!
    flask fab create-admin \
        --username admin \
        --firstname admin \
        --lastname admin \
        --email admin@matheworkout.at \
        --password ${FLASK_ADMIN_PASSWORD:-$(tr -dc A-Za-z0-9 </dev/urandom | head -c 20; echo)}
fi
