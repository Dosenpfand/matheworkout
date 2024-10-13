#!/bin/sh

# TODO: really a good idea to bootstrap if upgrade fails?
flask db upgrade \
    || ( flask fab create-db \
        && flask fab create-admin --username admin --firstname admin --lastname admin --email admin@matheworkout.at --password password )
