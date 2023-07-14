#!/bin/sh

flask db upgrade || flask fab create-db
