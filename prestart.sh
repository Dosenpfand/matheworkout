#!/bin/sh

flask db upgrade \
    || ( flask fab create-db \
        && flask fab create-admin --username admin --firstname admin --lastname admin --email admin@matheworkout.at --password password )
