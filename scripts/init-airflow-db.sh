#!/bin/bash
set -e

# Cria o banco de dados para o Airflow (se não existir)
psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" <<-EOSQL
    CREATE DATABASE airflow_db;
    GRANT ALL PRIVILEGES ON DATABASE airflow_db TO $POSTGRES_USER;
EOSQL