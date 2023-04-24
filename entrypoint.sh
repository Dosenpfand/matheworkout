#! /usr/bin/env sh
set -e

service postgresql start

# TODO: check if user/db exists and exit!
# TODO: take pw from env!

sudo -u postgres createuser mathesuper
sudo -u postgres createdb matheueben
sudo -u postgres psql -c "alter user mathesuper with encrypted password '123456'; grant all privileges on database matheueben to mathesuper;"

# TODO: still fails!
flask fab create-db
flask init-db

service postgresql stop

exec "$@"