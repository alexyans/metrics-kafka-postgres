#!/bin/bash

source .env

echo "---> Applying migrations..."
python pg_migrations.py
echo "---> Starting up metric sink..."
python sink.py
# TODO: external health check server that checks if PID is in process table
# echo "---> Starting up health check server..."
# start healthcheck script