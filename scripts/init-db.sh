#!/bin/bash
set -e

psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" <<-EOSQL
    CREATE DATABASE nanohire_api;
    GRANT ALL PRIVILEGES ON DATABASE nanohire_api TO postgres;
EOSQL

psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" <<-EOSQL
    CREATE DATABASE nanohire_integration;
    GRANT ALL PRIVILEGES ON DATABASE nanohire_integration TO postgres;
EOSQL

echo "Databases created successfully!"
