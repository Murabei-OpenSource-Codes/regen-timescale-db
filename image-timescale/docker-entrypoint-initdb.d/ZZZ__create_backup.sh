#!/bin/bash
set -e
echo "## Start creating backup database"
psql -v -U "$POSTGRES_USER" -d "$POSTGRES_DB" -c "SELECT timescaledb_pre_restore();"
psql -v -U "$POSTGRES_USER" -d "postgres" -c "SELECT pg_terminate_backend(pg_stat_activity.pid) FROM pg_stat_activity WHERE pid <> pg_backend_pid();"
psql -v -U "$POSTGRES_USER" -d "$POSTGRES_DB" -c 'SELECT timescaledb_post_restore();'
psql -v -U "$POSTGRES_USER" -d "postgres" -c "CREATE DATABASE backup WITH TEMPLATE $POSTGRES_DB;"
psql -v -U "$POSTGRES_USER" -d "postgres" -c "UPDATE pg_database SET datallowconn = 'false' WHERE datname = 'backup';"
echo "## Finish creating backup database"
