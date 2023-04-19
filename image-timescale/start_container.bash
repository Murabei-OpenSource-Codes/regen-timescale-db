#!/bin/bash
source wait-for-kong.bash

echo "Starting Flask server"
flask run --host=0.0.0.0 --port=5000 &

echo "Starting postgres server"
postgres ${POSTGRES_EXTRA_ARGS}
