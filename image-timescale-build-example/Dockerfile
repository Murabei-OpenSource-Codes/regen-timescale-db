FROM andrebaceti/regen-timescale-db:0.9.2

############################################
# Use the same values of the dumped database
# ENV KONG_API
ENV APP_NAME regen-test
ENV POSTGRES_USER="murabei"
ENV POSTGRES_DB="murabei"
ENV POSTGRES_PASSWORD="is_very_nice!"
ENV POSTGRES_EXTRA_ARGS="-c max_connections=1000 -c work_mem=50MB -c shared_buffers=1GB -c max_locks_per_transaction=500 -c max_locks_per_transaction=500 -c synchronous_commit=off -c max_wal_size=10GB -c min_wal_size=80MB"



#################################################################
# Copy the dumpfile to docker-entrypoint-initdb.d so
# the dumped database will be recriated when the container starts
COPY database/database.sql /docker-entrypoint-initdb.d/AAA__database.sql
