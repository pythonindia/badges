#! /usr/bin/env bash

HOST=${HOST:-0.0.0.0}
PORT=${PORT:-8000}

gunicorn badges.wsgi:app --bind $HOST:$PORT $@
