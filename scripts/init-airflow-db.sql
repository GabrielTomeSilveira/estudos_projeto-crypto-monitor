-- scripts/init-airflow-db.sql
-- Cria o banco de dados para o Airflow se não existir
\c postgres
SELECT 'CREATE DATABASE airflow_db'
WHERE NOT EXISTS (SELECT FROM pg_database WHERE datname = 'airflow_db')\gexec
GRANT ALL PRIVILEGES ON DATABASE airflow_db TO :"POSTGRES_USER";